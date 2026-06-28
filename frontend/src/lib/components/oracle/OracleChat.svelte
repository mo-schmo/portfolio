<script lang="ts">
	import { tick, onDestroy } from "svelte";
	import { fade, fly } from "svelte/transition";
	import {
		streamSSE,
		getSessionId,
		type StreamEvent,
	} from "$lib/api/agents";
	import ToolCallTrace from "./ToolCallTrace.svelte";

	export const bot: "concierge" | "tour" | "patent" = "concierge";
	export let endpoint: string;
	export let title: string;
	export let subtitle: string = "";
	export let placeholder: string = "Pose your question to the oracle...";
	export let initialPrompts: string[] = [];
	export let extraBody: Record<string, unknown> = {};

	interface Citation {
		id: string;
		title: string;
		href?: string;
		snippet?: string;
	}

	interface ToolInvocation {
		id: string;
		tool: string;
		args: Record<string, unknown>;
		result?: { ok: boolean; summary: string };
	}

	interface Turn {
		role: "user" | "assistant";
		content: string;
		citations?: Citation[];
		tools?: ToolInvocation[];
		streaming?: boolean;
	}

	let history: Turn[] = [];
	let input = "";
	let sending = false;
	let controller: AbortController | null = null;
	let scrollEl: HTMLDivElement | null = null;
	let inputEl: HTMLTextAreaElement | null = null;

	async function scrollToBottom() {
		await tick();
		if (scrollEl) scrollEl.scrollTop = scrollEl.scrollHeight;
	}

	async function send(prompt?: string) {
		const message = (prompt ?? input).trim();
		if (!message || sending) return;
		input = "";
		sending = true;
		controller = new AbortController();

		const userTurn: Turn = { role: "user", content: message };
		const assistantTurn: Turn = {
			role: "assistant",
			content: "",
			citations: [],
			tools: [],
			streaming: true,
		};
		history = [...history, userTurn, assistantTurn];
		scrollToBottom();

		const body = {
			session_id: getSessionId(),
			message,
			...extraBody,
		};

		try {
			for await (const event of streamSSE({
				path: endpoint,
				body,
				signal: controller.signal,
			})) {
				applyEvent(assistantTurn, event);
				history = [...history];
				scrollToBottom();
				if (event.type === "done" || event.type === "error") break;
			}
		} catch (err) {
			if ((err as Error).name !== "AbortError") {
				assistantTurn.content +=
					"\n\n(The wire was cut. Please try again.)";
			}
		} finally {
			assistantTurn.streaming = false;
			history = [...history];
			sending = false;
			controller = null;
			inputEl?.focus();
		}
	}

	function applyEvent(turn: Turn, event: StreamEvent) {
		switch (event.type) {
			case "token":
				turn.content += event.text;
				break;
			case "citation":
				turn.citations = [
					...(turn.citations ?? []),
					{
						id: event.id,
						title: event.title,
						href: event.href,
						snippet: event.snippet,
					},
				];
				break;
			case "tool_call":
				turn.tools = [
					...(turn.tools ?? []),
					{
						id: event.id ?? `${turn.tools?.length ?? 0}`,
						tool: event.tool,
						args: event.args,
					},
				];
				break;
			case "tool_result": {
				const last = turn.tools?.findLast?.(
					(t) => t.tool === event.tool && !t.result,
				);
				if (last) {
					last.result = { ok: event.ok, summary: event.summary };
				}
				break;
			}
			case "error":
				turn.content += `\n\n_Error: ${event.message}_`;
				break;
		}
	}

	function cancel() {
		controller?.abort();
	}

	function handleKey(e: KeyboardEvent) {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault();
			send();
		}
	}

	function reset() {
		history = [];
		input = "";
	}

	onDestroy(() => controller?.abort());
</script>

<div class="legal-folio bg-white/60 flex flex-col h-[640px] max-h-[80vh]">
	<header
		class="border-b border-paper-line px-6 py-4 flex items-baseline justify-between gap-4"
	>
		<div>
			<div
				class="text-xs font-display tracking-[0.3em] text-brass uppercase mb-1"
			>
				Counsel in Session
			</div>
			<h2
				class="text-xl md:text-2xl font-display font-black text-mahogany uppercase tracking-tight"
			>
				{title}
			</h2>
			{#if subtitle}
				<p class="text-sm text-mahogany/60 font-serif italic mt-1">
					{subtitle}
				</p>
			{/if}
		</div>
		{#if history.length > 0}
			<button
				on:click={reset}
				class="text-xs font-display tracking-widest uppercase text-mahogany/60 hover:text-mahogany transition-colors"
			>
				Clear Record
			</button>
		{/if}
	</header>

	<div bind:this={scrollEl} class="flex-grow overflow-y-auto px-6 py-6 oracle-transcript">
		{#if history.length === 0}
			<div in:fade={{ duration: 300 }} class="space-y-6">
				<p class="text-mahogany/70 font-serif italic leading-relaxed">
					The oracle is ready to hear your inquiry. Begin a fresh
					line of questioning, or select a prepared prompt below.
				</p>
				{#if initialPrompts.length > 0}
					<div class="space-y-3">
						<div
							class="text-[10px] font-display tracking-[0.3em] uppercase text-brass"
						>
							Suggested Inquiries
						</div>
						{#each initialPrompts as prompt}
							<button
								on:click={() => send(prompt)}
								class="block w-full text-left p-4 border border-paper-line bg-parchment/40 hover:bg-parchment hover:border-mahogany/40 transition-all font-serif italic text-mahogany"
							>
								{prompt}
							</button>
						{/each}
					</div>
				{/if}
			</div>
		{:else}
			<ul class="space-y-8">
				{#each history as turn, i (i)}
					<li in:fly={{ y: 6, duration: 200 }}>
						{#if turn.role === "user"}
							<div class="flex justify-end">
								<div
									class="max-w-[80%] px-5 py-3 bg-mahogany text-parchment font-serif leading-relaxed shadow-[2px_2px_0_rgba(45,27,27,0.15)]"
								>
									{turn.content}
								</div>
							</div>
						{:else}
							<div>
								{#if turn.tools && turn.tools.length > 0}
									<ToolCallTrace tools={turn.tools} />
								{/if}
								<div
									class="font-serif text-ink leading-relaxed whitespace-pre-wrap"
								>
									{turn.content}{#if turn.streaming}<span
											class="typewriter-cursor"></span
										>{/if}
								</div>
								{#if turn.citations && turn.citations.length > 0}
									<div
										class="mt-5 pt-4 border-t border-paper-line/70"
									>
										<div
											class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-2"
										>
											Citations on the Record
										</div>
										<div class="flex flex-wrap gap-2">
											{#each turn.citations as cite}
												{#if cite.href}
													<a
														href={cite.href}
														title={cite.snippet ?? ""}
														class="text-xs font-display tracking-wider uppercase px-3 py-1 border border-mahogany/30 text-mahogany hover:bg-mahogany hover:text-parchment transition-all"
													>
														{cite.title}
													</a>
												{:else}
													<span
														title={cite.snippet ?? ""}
														class="text-xs font-display tracking-wider uppercase px-3 py-1 border border-mahogany/30 text-mahogany/70"
													>
														{cite.title}
													</span>
												{/if}
											{/each}
										</div>
									</div>
								{/if}
							</div>
						{/if}
					</li>
				{/each}
			</ul>
		{/if}
	</div>

	<footer class="border-t border-paper-line px-6 py-4 bg-parchment/40">
		<div class="flex items-end gap-3">
			<textarea
				bind:this={inputEl}
				bind:value={input}
				on:keydown={handleKey}
				rows="2"
				disabled={sending}
				{placeholder}
				class="flex-grow resize-none bg-white/80 border border-paper-line focus:border-mahogany focus:outline-none px-4 py-3 font-serif text-ink leading-relaxed"
			></textarea>
			{#if sending}
				<button
					on:click={cancel}
					class="btn-outline-legal !px-5 !py-3 !text-xs"
				>
					Halt
				</button>
			{:else}
				<button
					on:click={() => send()}
					disabled={!input.trim()}
					class="btn-legal !px-5 !py-3 !text-xs disabled:opacity-40 disabled:cursor-not-allowed"
				>
					Submit
				</button>
			{/if}
		</div>
	</footer>
</div>
