<script lang="ts">
	import { onDestroy } from "svelte";
	import { fly, fade } from "svelte/transition";
	import { streamSSE, getSessionId } from "$lib/api/agents";

	// --- Domain types mirrored from agents/app/schemas/patent.py ---
	type Severity = "low" | "medium" | "high";

	interface Finding {
		severity: Severity;
		rule: string;
		location: string;
		description: string;
		recommendation: string;
	}

	interface ComplianceReport {
		overall: Severity;
		summary: string;
		findings: Finding[];
	}

	interface RevisionResult {
		revised_claims: string[];
		revised_abstract: string;
		change_log: string[];
	}

	interface PatentSections {
		title: string;
		abstract: string;
		field_of_invention: string;
		background: string;
		summary: string;
		detailed_description: string;
		drawings_description: string;
		claims: string[];
		notes: string;
	}

	interface ReportPayload {
		sections: PatentSections | null;
		report: ComplianceReport | null;
		revision: RevisionResult | null;
		iterations: number;
	}

	interface TimelineEntry {
		node: string;
		label: string;
		status: "running" | "done";
		summary?: string;
		startedAt: number;
		finishedAt?: number;
	}

	const sampleDrafts: { name: string; description: string; draft: string }[] = [
		{
			name: "Sample I - Smart Coffee Mug",
			description:
				"A toy electronics application with antecedent-basis bugs and a vague claim 1.",
			draft: `Title: Temperature-regulating beverage container

Abstract: A mug that keeps coffee hot using a fancy new system.

Field: The invention relates to drinkware.

Summary: The invention is a mug.

Detailed description: A vessel contains a heating element. The heating element is powered by a battery. The battery is rechargeable. A controller adjusts the heating element. A user adjusts the temperature.

Claims:
1. A mug, comprising the heating element and the battery, wherein the controller controls the temperature.
2. The mug of claim 1, wherein the user sets the desired temperature.
3. The mug, wherein the controller is wireless.`,
		},
		{
			name: "Sample II - Software Method",
			description:
				"A software-method claim missing structure under 35 USC 112(f) concerns.",
			draft: `Title: Method for predicting user churn

Abstract: This invention predicts when a user will stop using a service so the service can do something about it.

Detailed description: Data about the user is collected. A model processes the data. A prediction is output. Means for collecting data, means for processing data, and means for outputting a prediction are provided.

Claims:
1. A method for predicting user churn, comprising:
  - means for collecting data from the user;
  - means for processing the data; and
  - means for outputting a prediction.
2. The method of claim 1, wherein the data is collected over time.`,
		},
		{
			name: "Sample III - Clean Mechanical Claim",
			description:
				"A relatively well-formed mechanical claim; mostly low/medium findings expected.",
			draft: `Title: Self-aligning bicycle pedal

Abstract: A bicycle pedal having a spring-biased platform that returns to a level orientation when not under load, easing rider remount after a stop.

Field of the invention: Bicycle componentry.

Background: Conventional platform pedals can rotate freely about the spindle when not under load, requiring riders to flip the pedal with their foot before remounting after a stop.

Summary: A bicycle pedal includes a body rotatable about a spindle, a torsion spring engaging the body and the spindle to bias the body into a level orientation when no load is applied, and a damper limiting return speed.

Detailed description: The pedal includes a spindle defining a rotation axis, a body rotatably mounted on the spindle, a torsion spring having a first end fixed to the spindle and a second end engaging the body, and a viscous damper coupled between the body and the spindle to limit angular velocity of the body relative to the spindle.

Claims:
1. A bicycle pedal, comprising:
  a spindle defining a rotation axis;
  a body rotatably mounted on the spindle;
  a torsion spring having a first end fixed to the spindle and a second end engaging the body, the torsion spring biasing the body into a level orientation in the absence of rider load; and
  a damper coupled between the body and the spindle.
2. The bicycle pedal of claim 1, wherein the damper comprises a viscous damper.
3. The bicycle pedal of claim 1, further comprising a stop limiting rotation of the body relative to the spindle.`,
		},
	];

	let draft = "";
	let running = false;
	let timeline: TimelineEntry[] = [];
	let payload: ReportPayload | null = null;
	let errorMessage = "";
	let controller: AbortController | null = null;
	let activeSampleIndex = -1;

	function loadSample(i: number) {
		activeSampleIndex = i;
		draft = sampleDrafts[i].draft;
	}

	function resetRun() {
		timeline = [];
		payload = null;
		errorMessage = "";
	}

	async function runBench() {
		if (running || !draft.trim()) return;
		running = true;
		resetRun();
		controller = new AbortController();

		try {
			for await (const event of streamSSE({
				path: "/agents/patent/run",
				body: { draft, session_id: getSessionId() },
				signal: controller.signal,
			})) {
				applyEvent(event);
				if (event.type === "done" || event.type === "error") break;
			}
		} catch (err) {
			if ((err as Error).name !== "AbortError") {
				errorMessage = (err as Error).message;
			}
		} finally {
			running = false;
			controller = null;
		}
	}

	function applyEvent(event: any) {
		if (event.type === "state") {
			const now = Date.now();
			if (event.status === "running") {
				timeline = [
					...timeline,
					{
						node: event.node,
						label: event.label ?? event.node,
						status: "running",
						startedAt: now,
					},
				];
			} else if (event.status === "done") {
				// Mark the most recent running entry for this node as done.
				const i = [...timeline]
					.reverse()
					.findIndex(
						(t) => t.node === event.node && t.status === "running",
					);
				if (i !== -1) {
					const idx = timeline.length - 1 - i;
					timeline[idx] = {
						...timeline[idx],
						status: "done",
						summary: event.summary,
						finishedAt: now,
					};
					timeline = [...timeline];
				}
			}
		} else if (event.type === "report") {
			payload = {
				sections: event.sections ?? null,
				report: event.report ?? null,
				revision: event.revision ?? null,
				iterations: event.iterations ?? 0,
			};
		} else if (event.type === "error") {
			errorMessage = event.message ?? "The bench reported an error.";
		}
	}

	function cancel() {
		controller?.abort();
	}

	function elapsed(t: TimelineEntry): string {
		if (!t.finishedAt) return "...";
		const ms = t.finishedAt - t.startedAt;
		return ms < 1000 ? `${ms}ms` : `${(ms / 1000).toFixed(1)}s`;
	}

	function severityClass(s: Severity | string | undefined): string {
		switch ((s ?? "").toLowerCase()) {
			case "high":
				return "severity-high";
			case "medium":
				return "severity-medium";
			default:
				return "severity-low";
		}
	}

	onDestroy(() => controller?.abort());
</script>

<svelte:head>
	<title>Patent Compliance Bench - The Oracles</title>
	<meta
		name="description"
		content="A multi-agent compliance bench - Drafter, Reviewer, and Revisor - reviews a draft patent application and returns a structured memorandum."
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
			Oracle II &middot; Multi-Agent Bench
		</div>
		<h1
			class="text-5xl md:text-7xl font-display font-black mb-4 text-mahogany tracking-tighter uppercase"
		>
			Patent Compliance Bench
		</h1>
		<div class="w-24 h-1 bg-mahogany mx-auto mb-6"></div>
		<p
			class="text-lg text-mahogany/80 font-serif italic max-w-3xl mx-auto leading-relaxed"
		>
			A Drafter parses the application. A Reviewer issues a structured
			compliance memorandum. If high-severity findings remain, a Revisor
			proposes amendments and the Reviewer reconvenes.
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
				This is a demonstrator. Do not paste confidential or
				attorney-privileged drafts. The bench does not provide legal
				advice, does not establish an attorney-client relationship,
				and may be wrong. Use only sample or fictitious drafts.
			</p>
		</div>
	</section>

	<!-- Three panel layout -->
	<div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
		<!-- LEFT: draft input -->
		<section class="xl:col-span-4">
			<div class="legal-folio bg-white/60 p-6 sticky top-24">
				<div
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-2"
				>
					Exhibit A
				</div>
				<h2
					class="text-xl font-display font-black text-mahogany uppercase tracking-tight mb-4"
				>
					Draft Application
				</h2>

				<div class="mb-4">
					<div
						class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-2"
					>
						Sample Drafts
					</div>
					<div class="flex flex-wrap gap-2">
						{#each sampleDrafts as s, i}
							<button
								on:click={() => loadSample(i)}
								class="text-xs font-display tracking-wider uppercase px-3 py-1.5 border transition-all {activeSampleIndex ===
								i
									? 'border-mahogany bg-mahogany text-parchment'
									: 'border-paper-line text-mahogany hover:border-mahogany'}"
								title={s.description}
							>
								{s.name.split(" - ")[0]}
							</button>
						{/each}
					</div>
					{#if activeSampleIndex >= 0}
						<p
							class="mt-2 text-xs text-mahogany/60 font-serif italic"
							in:fade={{ duration: 120 }}
						>
							{sampleDrafts[activeSampleIndex].description}
						</p>
					{/if}
				</div>

				<label
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass block mb-2"
					for="draft-input"
				>
					Paste a (fictitious) draft
				</label>
				<textarea
					id="draft-input"
					bind:value={draft}
					rows="14"
					disabled={running}
					placeholder="Title: ...&#10;Abstract: ...&#10;Claims:&#10;1. ..."
					class="w-full bg-white border border-paper-line focus:border-mahogany focus:outline-none px-4 py-3 font-mono text-xs text-ink leading-relaxed mb-4"
				></textarea>

				<div class="flex items-center gap-3">
					{#if running}
						<button
							on:click={cancel}
							class="btn-outline-legal !px-5 !py-3 !text-xs"
						>
							Adjourn
						</button>
					{:else}
						<button
							on:click={runBench}
							disabled={!draft.trim()}
							class="btn-legal !px-5 !py-3 !text-xs disabled:opacity-40 disabled:cursor-not-allowed"
						>
							Convene the Bench
						</button>
					{/if}
					<span class="text-xs text-mahogany/50 font-serif italic">
						{draft.length} chars
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

		<!-- MIDDLE: timeline -->
		<section class="xl:col-span-3">
			<div class="legal-folio bg-white/60 p-6 min-h-[400px]">
				<div
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-2"
				>
					Proceedings
				</div>
				<h2
					class="text-xl font-display font-black text-mahogany uppercase tracking-tight mb-6"
				>
					Bench Timeline
				</h2>

				{#if timeline.length === 0}
					<p
						class="font-serif italic text-mahogany/60 text-sm leading-relaxed"
					>
						The bench is not yet in session. Load a sample draft or
						paste one, then convene the bench to begin.
					</p>
				{:else}
					<ol class="space-y-5 telegraph-wire pl-4">
						{#each timeline as entry, i (i)}
							<li
								in:fly={{ y: 4, duration: 220 }}
								class="relative"
							>
								<div class="flex items-baseline gap-2">
									<span
										class="inline-block w-2 h-2 rounded-full"
										class:bg-brass={entry.status === "done"}
										class:bg-mahogany={entry.status ===
											"running"}
										class:animate-pulse={entry.status ===
											"running"}
									></span>
									<span
										class="text-[10px] font-display tracking-[0.3em] uppercase text-brass"
									>
										{entry.label}
									</span>
									<span
										class="text-[10px] font-mono text-mahogany/40 ml-auto"
									>
										{elapsed(entry)}
									</span>
								</div>
								<p
									class="mt-1 font-serif text-sm text-ink/85 leading-snug"
								>
									{#if entry.summary}
										{entry.summary}
									{:else if entry.status === "running"}
										<span class="italic text-mahogany/60">
											deliberating...
										</span>
									{/if}
								</p>
							</li>
						{/each}
					</ol>
				{/if}
			</div>
		</section>

		<!-- RIGHT: memorandum -->
		<section class="xl:col-span-5">
			<div class="legal-folio bg-white/70 p-8 md:p-10 min-h-[400px]">
				<div
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-2"
				>
					Memorandum
				</div>
				<h2
					class="text-2xl font-display font-black text-mahogany uppercase tracking-tight mb-6"
				>
					Compliance Memorandum
				</h2>

				{#if !payload}
					<p
						class="font-serif italic text-mahogany/60 text-sm leading-relaxed"
					>
						The memorandum will be filed once the bench has
						completed its review.
					</p>
				{:else}
					{@const report = payload.report}
					{#if report}
						<div in:fade={{ duration: 240 }}>
							<div
								class="flex items-center gap-3 pb-4 mb-6 border-b border-paper-line"
							>
								<span
									class="text-[10px] font-display tracking-[0.3em] uppercase {severityClass(
										report.overall,
									)}"
								>
									Overall: {(report.overall ?? "low").toUpperCase()}
								</span>
								{#if payload.iterations > 0}
									<span
										class="text-[10px] font-display tracking-[0.3em] uppercase text-mahogany/50"
									>
										{payload.iterations} revision{payload.iterations >
										1
											? "s"
											: ""}
									</span>
								{/if}
							</div>

							<p
								class="font-serif text-base md:text-lg leading-relaxed text-ink/90 italic mb-8"
							>
								{report.summary}
							</p>

							{#if report.findings && report.findings.length > 0}
								<h3
									class="text-xs font-display tracking-[0.3em] uppercase text-brass mb-4"
								>
									Findings ({report.findings.length})
								</h3>
								<ul class="space-y-5">
									{#each report.findings as f}
										<li
											class="border-l-2 pl-4 border-paper-line"
										>
											<div
												class="flex items-baseline justify-between gap-3 mb-1"
											>
												<span
													class="text-[10px] font-display tracking-[0.3em] uppercase {severityClass(
														f.severity,
													)}"
												>
													{f.severity?.toUpperCase()} &middot; {f.rule}
												</span>
												<span
													class="text-[10px] font-mono text-mahogany/40 whitespace-nowrap"
												>
													{f.location}
												</span>
											</div>
											<p
												class="font-serif text-sm text-ink/90 mb-2 leading-snug"
											>
												{f.description}
											</p>
											<p
												class="font-serif text-xs italic text-mahogany/70 leading-snug"
											>
												Recommendation: {f.recommendation}
											</p>
										</li>
									{/each}
								</ul>
							{/if}

							{#if payload.revision && (payload.revision.revised_claims.length > 0 || payload.revision.revised_abstract || payload.revision.change_log.length > 0)}
								<div
									class="mt-10 pt-6 border-t border-paper-line"
								>
									<h3
										class="text-xs font-display tracking-[0.3em] uppercase text-brass mb-4"
									>
										Proposed Revision
									</h3>

									{#if payload.revision.change_log.length > 0}
										<div class="mb-6">
											<div
												class="text-[10px] font-display tracking-[0.3em] uppercase text-mahogany/60 mb-2"
											>
												Change Log
											</div>
											<ul
												class="list-disc list-inside space-y-1 font-serif text-sm text-ink/90"
											>
												{#each payload.revision.change_log as c}
													<li>{c}</li>
												{/each}
											</ul>
										</div>
									{/if}

									{#if payload.revision.revised_abstract}
										<div class="mb-6">
											<div
												class="text-[10px] font-display tracking-[0.3em] uppercase text-mahogany/60 mb-2"
											>
												Revised Abstract
											</div>
											<p
												class="font-serif text-sm text-ink/90 italic leading-relaxed"
											>
												{payload.revision.revised_abstract}
											</p>
										</div>
									{/if}

									{#if payload.revision.revised_claims.length > 0}
										<div>
											<div
												class="text-[10px] font-display tracking-[0.3em] uppercase text-mahogany/60 mb-2"
											>
												Revised Claims
											</div>
											<ol
												class="space-y-3 font-serif text-sm text-ink/90"
											>
												{#each payload.revision.revised_claims as claim, idx}
													<li>
														<span class="font-bold"
															>{idx + 1}.</span
														>
														{claim}
													</li>
												{/each}
											</ol>
										</div>
									{/if}
								</div>
							{/if}
						</div>
					{:else}
						<p
							class="font-serif italic text-mahogany/60 text-sm leading-relaxed"
						>
							The bench returned no report. Please try a
							different draft.
						</p>
					{/if}
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
