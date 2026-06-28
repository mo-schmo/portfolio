<script lang="ts">
	import { slide } from "svelte/transition";

	export let tools: {
		id: string;
		tool: string;
		args: Record<string, unknown>;
		result?: { ok: boolean; summary: string };
	}[] = [];

	let expanded = false;

	function formatArgs(args: Record<string, unknown>): string {
		try {
			return JSON.stringify(args, null, 2);
		} catch {
			return String(args);
		}
	}
</script>

<div class="mb-5 border-l-2 border-brass/50 pl-4 telegraph-wire">
	<button
		class="flex items-center gap-3 text-[10px] font-display font-bold tracking-[0.3em] uppercase text-brass hover:text-mahogany transition-colors w-full text-left"
		on:click={() => (expanded = !expanded)}
	>
		<span class="inline-block w-2 h-2 rounded-full bg-brass animate-pulse"></span>
		<span>Tools on the Wire ({tools.length})</span>
		<span class="text-mahogany/40">{expanded ? "[hide]" : "[show]"}</span>
	</button>

	{#if expanded}
		<ul transition:slide={{ duration: 200 }} class="mt-3 space-y-3">
			{#each tools as t (t.id)}
				<li class="font-mono text-xs">
					<div class="flex items-baseline gap-2">
						<span class="text-brass">&gt;</span>
						<span class="text-mahogany font-bold">{t.tool}</span>
						<span class="text-mahogany/50">(</span>
					</div>
					<pre
						class="text-mahogany/70 pl-5 pt-1 pb-1 whitespace-pre-wrap break-words text-[11px] leading-snug">{formatArgs(t.args)}</pre>
					<div class="text-mahogany/50 pl-1">)</div>
					{#if t.result}
						<div
							class="pl-5 mt-1 text-[11px] {t.result.ok
								? 'text-mahogany/80'
								: 'text-red-800'}"
						>
							<span class="text-brass">&larr;</span>
							{t.result.summary}
						</div>
					{:else}
						<div
							class="pl-5 mt-1 text-[11px] text-mahogany/40 italic"
						>
							<span class="text-brass">&larr;</span>
							awaiting return...
						</div>
					{/if}
				</li>
			{/each}
		</ul>
	{/if}
</div>
