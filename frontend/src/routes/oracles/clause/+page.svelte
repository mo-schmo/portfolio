<script lang="ts">
	import { fade, fly } from "svelte/transition";
	import { explainClause, type ClauseExplanation } from "$lib/api/agents";

	const sampleClauses: { name: string; clause: string }[] = [
		{
			name: "Indemnification",
			clause: `Licensee shall indemnify, defend, and hold harmless Licensor and its affiliates from and against any and all claims, damages, liabilities, costs, and expenses (including reasonable attorneys' fees) arising out of or related to Licensee's use of the Software, regardless of the cause and even if such claims arise from the negligence of Licensor.`,
		},
		{
			name: "Auto-Renewal",
			clause: `This Agreement shall automatically renew for successive one (1) year terms unless either party provides written notice of non-renewal at least ninety (90) days prior to the end of the then-current term. Upon renewal, fees may increase by up to fifteen percent (15%) per term at Provider's sole discretion.`,
		},
		{
			name: "Limitation of Liability",
			clause: `In no event shall either party's aggregate liability arising out of or related to this Agreement exceed the total fees paid by Customer in the twelve (12) months preceding the event giving rise to the claim. Neither party shall be liable for any indirect, incidental, consequential, or punitive damages.`,
		},
	];

	let clause = "";
	let loading = false;
	let result: ClauseExplanation | null = null;
	let errorMessage = "";
	let controller: AbortController | null = null;
	let activeSampleIndex = -1;

	function loadSample(i: number) {
		activeSampleIndex = i;
		clause = sampleClauses[i].clause;
	}

	async function submit() {
		if (loading || !clause.trim()) return;
		loading = true;
		result = null;
		errorMessage = "";
		controller = new AbortController();
		try {
			result = await explainClause(clause, controller.signal);
		} catch (err) {
			if ((err as Error).name !== "AbortError") {
				errorMessage = (err as Error).message;
			}
		} finally {
			loading = false;
			controller = null;
		}
	}

	function cancel() {
		controller?.abort();
	}

	function severityClass(s: string | undefined): string {
		switch ((s ?? "").toLowerCase()) {
			case "high":
				return "severity-high";
			case "medium":
				return "severity-medium";
			default:
				return "severity-low";
		}
	}
</script>

<svelte:head>
	<title>Clause Explainer - The Oracles</title>
	<meta
		name="description"
		content="Paste a contract clause and receive a structured memorandum: plain English, enumerated obligations, flagged risks, and suggested redlines."
	/>
</svelte:head>

<div class="container mx-auto px-4 py-20 max-w-7xl">
	<!-- Header -->
	<section class="text-center mb-10">
		<a
			href="/oracles"
			class="text-xs font-display tracking-[0.4em] text-brass uppercase hover:text-mahogany transition-colors"
		>
			&larr; The Chambers
		</a>
		<div
			class="text-xs font-display tracking-[0.4em] text-brass uppercase mt-6 mb-3"
		>
			Oracle IV &middot; Structured Output
		</div>
		<h1
			class="text-5xl md:text-7xl font-display font-black mb-4 text-mahogany tracking-tighter uppercase"
		>
			Clause Explainer
		</h1>
		<div class="w-24 h-1 bg-mahogany mx-auto mb-6"></div>
		<p
			class="text-lg text-mahogany/80 font-serif italic max-w-3xl mx-auto leading-relaxed"
		>
			Submit a single contract clause; receive a memorandum of counsel -
			plain English, obligations enumerated, risks flagged, and redlines
			proposed - returned as a single validated JSON object.
		</p>
	</section>

	<!-- Disclaimer -->
	<section class="mb-10">
		<div
			class="legal-folio bg-parchment/80 border-l-4 border-mahogany p-5 md:p-6 max-w-4xl mx-auto"
		>
			<div
				class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-2"
			>
				Notice from the Bench
			</div>
			<p
				class="font-serif italic text-mahogany/90 leading-relaxed text-sm md:text-base"
			>
				This is a demonstrator. It does not provide legal advice, does
				not establish an attorney-client relationship, and may be wrong.
				Use sample or fictitious clauses; do not paste confidential
				agreements.
			</p>
		</div>
	</section>

	<!-- Two-pane layout -->
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
		<!-- LEFT: clause input -->
		<section>
			<div class="legal-folio bg-white/60 p-6 md:p-8 sticky top-24">
				<div
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-2"
				>
					The Clause
				</div>
				<h2
					class="text-xl font-display font-black text-mahogany uppercase tracking-tight mb-4"
				>
					Submit for Review
				</h2>

				<div class="mb-4">
					<div
						class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-2"
					>
						Sample Clauses
					</div>
					<div class="flex flex-wrap gap-2">
						{#each sampleClauses as s, i}
							<button
								on:click={() => loadSample(i)}
								class="text-xs font-display tracking-wider uppercase px-3 py-1.5 border transition-all {activeSampleIndex ===
								i
									? 'border-mahogany bg-mahogany text-parchment'
									: 'border-paper-line text-mahogany hover:border-mahogany'}"
							>
								{s.name}
							</button>
						{/each}
					</div>
				</div>

				<label
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass block mb-2"
					for="clause-input"
				>
					Paste a (fictitious) clause
				</label>
				<textarea
					id="clause-input"
					bind:value={clause}
					rows="12"
					disabled={loading}
					placeholder="Licensee shall indemnify and hold harmless..."
					class="w-full bg-white border border-paper-line focus:border-mahogany focus:outline-none px-4 py-3 font-serif text-sm text-ink leading-relaxed mb-4"
				></textarea>

				<div class="flex items-center gap-3">
					{#if loading}
						<button
							on:click={cancel}
							class="btn-outline-legal !px-5 !py-3 !text-xs"
						>
							Withdraw
						</button>
					{:else}
						<button
							on:click={submit}
							disabled={!clause.trim()}
							class="btn-legal !px-5 !py-3 !text-xs disabled:opacity-40 disabled:cursor-not-allowed"
						>
							Request Memorandum
						</button>
					{/if}
					<span class="text-xs text-mahogany/50 font-serif italic">
						{clause.length} chars
					</span>
				</div>

				{#if errorMessage}
					<div
						class="mt-4 p-3 border border-red-900/30 bg-red-50/50 text-red-900 text-xs font-serif"
					>
						{errorMessage}
					</div>
				{/if}
			</div>
		</section>

		<!-- RIGHT: memorandum -->
		<section>
			<div class="legal-folio bg-white/70 p-8 md:p-10 min-h-[400px]">
				<div
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-2"
				>
					Memorandum of Counsel
				</div>
				<h2
					class="text-2xl font-display font-black text-mahogany uppercase tracking-tight mb-6"
				>
					Plain-English Reading
				</h2>

				{#if loading}
					<div class="space-y-3" in:fade={{ duration: 150 }}>
						<p
							class="font-serif italic text-mahogany/60 text-sm leading-relaxed"
						>
							Counsel is reviewing the clause and preparing the
							memorandum<span class="typewriter-cursor"></span>
						</p>
					</div>
				{:else if !result}
					<p
						class="font-serif italic text-mahogany/60 text-sm leading-relaxed"
					>
						The memorandum will appear here once a clause has been
						submitted for review. Load a sample clause or paste your
						own to begin.
					</p>
				{:else}
					<div in:fade={{ duration: 240 }} class="space-y-8">
						<!-- Summary -->
						<div>
							<h3
								class="text-xs font-display tracking-[0.3em] uppercase text-brass mb-2"
							>
								In Short
							</h3>
							<p
								class="font-serif text-base md:text-lg leading-relaxed text-ink/90 italic"
							>
								{result.clause_summary}
							</p>
						</div>

						<!-- Plain English -->
						<div>
							<h3
								class="text-xs font-display tracking-[0.3em] uppercase text-brass mb-2"
							>
								Plain English
							</h3>
							<p
								class="font-serif text-base leading-relaxed text-ink/90"
							>
								{result.plain_english}
							</p>
						</div>

						<!-- Obligations -->
						{#if result.obligations?.length}
							<div>
								<h3
									class="text-xs font-display tracking-[0.3em] uppercase text-brass mb-3"
								>
									Obligations ({result.obligations.length})
								</h3>
								<ul class="space-y-3">
									{#each result.obligations as o, i (i)}
										<li
											in:fly={{ y: 4, duration: 180, delay: i * 40 }}
											class="border-l-2 pl-4 border-paper-line"
										>
											<span
												class="text-[10px] font-display tracking-[0.2em] uppercase text-mahogany font-bold"
											>
												{o.party}
											</span>
											<p
												class="font-serif text-sm text-ink/90 leading-snug mt-1"
											>
												{o.obligation}
											</p>
										</li>
									{/each}
								</ul>
							</div>
						{/if}

						<!-- Risks -->
						{#if result.risks?.length}
							<div>
								<h3
									class="text-xs font-display tracking-[0.3em] uppercase text-brass mb-3"
								>
									Risks ({result.risks.length})
								</h3>
								<ul class="space-y-3">
									{#each result.risks as r, i (i)}
										<li
											in:fly={{ y: 4, duration: 180, delay: i * 40 }}
											class="border-l-2 pl-4 border-paper-line"
										>
											<span
												class="text-[10px] font-display tracking-[0.3em] uppercase {severityClass(
													r.severity,
												)}"
											>
												{(r.severity ?? "low").toUpperCase()}
											</span>
											<p
												class="font-serif text-sm text-ink/90 leading-snug mt-1"
											>
												{r.description}
											</p>
										</li>
									{/each}
								</ul>
							</div>
						{/if}

						<!-- Suggested redlines -->
						{#if result.suggested_redlines?.length}
							<div class="pt-2 border-t border-paper-line">
								<h3
									class="text-xs font-display tracking-[0.3em] uppercase text-brass mb-3 mt-4"
								>
									Suggested Redlines ({result.suggested_redlines
										.length})
								</h3>
								<ul class="space-y-5">
									{#each result.suggested_redlines as rl, i (i)}
										<li
											in:fly={{ y: 4, duration: 180, delay: i * 40 }}
											class="border border-paper-line bg-parchment/40 p-4"
										>
											<p
												class="font-mono text-xs text-red-900/80 line-through mb-2 leading-snug"
											>
												{rl.original}
											</p>
											<p
												class="font-mono text-xs text-mahogany mb-2 leading-snug"
											>
												{rl.suggestion}
											</p>
											<p
												class="font-serif text-xs italic text-mahogany/70 leading-snug"
											>
												{rl.rationale}
											</p>
										</li>
									{/each}
								</ul>
							</div>
						{/if}
					</div>
				{/if}
			</div>
		</section>
	</div>
</div>

<style>
	.severity-high {
		color: oklch(0.43 0.18 28);
	}
	.severity-medium {
		color: oklch(0.55 0.13 70);
	}
	.severity-low {
		color: oklch(0.45 0.07 145);
	}
</style>
