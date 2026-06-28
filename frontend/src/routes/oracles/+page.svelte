<script lang="ts">
	interface OracleEntry {
		number: string;
		discipline: string;
		title: string;
		summary: string;
		details: string[];
		stack: string[];
		status: "ready" | "in-chambers";
		href?: string;
	}

	const oracles: OracleEntry[] = [
		{
			number: "I",
			discipline: "Retrieval-Augmented Counsel",
			title: "Portfolio Concierge",
			summary:
				"An informed counsel that has read every page of this folio - resume, projects, and writings - and answers with citations to the record.",
			details: [
				"Grounded RAG over the entire portfolio",
				"Streamed answers with inline citation chips",
				"Returns to the source: clickable links to the cited record",
			],
			stack: [
				"sentence-transformers",
				"OpenRouter",
				"FastAPI",
				"SSE streaming",
			],
			status: "in-chambers",
		},
		{
			number: "II",
			discipline: "Multi-Agent Bench",
			title: "Patent Compliance Bench",
			summary:
				"Three counsels confer in chambers - a Drafter, a Reviewer, and a Revisor - and return a structured compliance memorandum on a draft patent application.",
			details: [
				"LangGraph workflow with critique loop",
				"Structured findings: severity, citation, recommendation",
				"Live timeline reveals each agent as it deliberates",
			],
			stack: [
				"LangGraph",
				"Pydantic structured output",
				"OpenRouter",
				"SSE state events",
			],
			status: "in-chambers",
		},
		{
			number: "III",
			discipline: "Tool-Using Agent",
			title: "Project Tour Guide",
			summary:
				"A guide who walks the halls of the works - retrieving the relevant records as you ask, with every tool call shown on the wire.",
			details: [
				"Calls tools against the Go backend (projects, blog)",
				"Reasoning + tool invocations rendered as a telegraph trace",
				"Per-project context, anchored to a specific exhibit",
			],
			stack: ["OpenRouter tool-use", "Go backend tools", "FastAPI"],
			status: "in-chambers",
		},
		{
			number: "IV",
			discipline: "Structured Output",
			title: "Clause Explainer",
			summary:
				"Paste a contract clause; receive a memorandum of counsel - plain English, obligations enumerated, risks flagged, redlines proposed.",
			details: [
				"Single-shot JSON-mode generation",
				"Risk-tiered findings with rationale",
				"Suggested redlines with reasoning preserved",
			],
			stack: ["JSON mode", "Pydantic schema", "FastAPI"],
			status: "in-chambers",
		},
	];
</script>

<svelte:head>
	<title>The Oracles - Mohammed Hamza</title>
	<meta
		name="description"
		content="Four agentic counsels - portfolio concierge, patent compliance bench, project tour guide, and clause explainer - housed inside the Hamza & Co. legal archive."
	/>
</svelte:head>

<div class="container mx-auto px-4 py-28 max-w-6xl">
	<!-- Hero -->
	<section
		class="text-center mb-24 border-b-4 border-double border-mahogany pb-16"
	>
		<div
			class="text-xs font-display tracking-[0.4em] text-brass uppercase mb-6"
		>
			Chambers of Counsel
		</div>
		<h1
			class="text-6xl md:text-8xl font-display font-black mb-6 text-mahogany tracking-tighter uppercase"
		>
			The Oracles
		</h1>
		<div class="w-32 h-1 bg-mahogany mx-auto mb-10"></div>
		<p
			class="text-xl text-mahogany/80 font-serif italic max-w-3xl mx-auto leading-relaxed"
		>
			Four agentic counsels reside within the archive. Each is its own
			discipline - retrieval, deliberation, instrumentation, and
			structured judgment - and each demonstrates a different facet of
			agentic AI engineering.
		</p>
	</section>

	<!-- The Bench -->
	<section class="mb-24">
		<div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
			{#each oracles as oracle}
				<article
					class="legal-folio bg-white/60 p-10 md:p-12 group oracle-illumination flex flex-col"
				>
					<header
						class="flex items-baseline justify-between gap-4 mb-6 pb-6 border-b border-paper-line"
					>
						<div>
							<div
								class="text-xs font-display tracking-[0.3em] text-brass uppercase mb-2"
							>
								Oracle {oracle.number} &middot; {oracle.discipline}
							</div>
							<h2
								class="text-3xl font-display font-black text-mahogany uppercase tracking-tight"
							>
								{oracle.title}
							</h2>
						</div>
						<span
							class="legal-stamp shrink-0 whitespace-nowrap"
							class:opacity-100={oracle.status === "ready"}
						>
							{oracle.status === "ready"
								? "In Session"
								: "In Chambers"}
						</span>
					</header>

					<p
						class="font-serif text-lg text-ink/85 italic leading-relaxed mb-8"
					>
						{oracle.summary}
					</p>

					<ul class="space-y-3 mb-8">
						{#each oracle.details as detail}
							<li class="flex items-start gap-3">
								<span
									class="mt-2 inline-block w-1.5 h-1.5 bg-brass shrink-0"
								></span>
								<span class="font-serif text-ink/90"
									>{detail}</span
								>
							</li>
						{/each}
					</ul>

					<div class="mt-auto pt-6 border-t border-paper-line">
						<div
							class="text-[10px] font-display tracking-[0.3em] text-brass uppercase mb-3"
						>
							Instruments of the Court
						</div>
						<div class="flex flex-wrap gap-2">
							{#each oracle.stack as tool}
								<span
									class="px-3 py-1 bg-mahogany/5 border border-mahogany/15 text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/70"
								>
									{tool}
								</span>
							{/each}
						</div>
					</div>
				</article>
			{/each}
		</div>
	</section>

	<!-- Notice -->
	<section class="mb-12">
		<div
			class="legal-folio bg-parchment/70 p-10 md:p-14 max-w-4xl mx-auto text-center"
		>
			<div
				class="text-xs font-display tracking-[0.4em] text-brass uppercase mb-4"
			>
				Notice from the Bench
			</div>
			<h2
				class="text-3xl font-display font-black text-mahogany uppercase tracking-tight mb-4"
			>
				Chambers Are Being Prepared
			</h2>
			<p class="font-serif text-lg text-ink/85 italic leading-relaxed">
				The oracles are presently in deliberation. The architecture is
				in place - a Python FastAPI sidecar wired to OpenRouter, a
				typed streaming client, and the Counsel aesthetic to greet you
				when each opens session. Please check back shortly.
			</p>
			<div class="mt-8 flex justify-center gap-6">
				<a href="/projects" class="btn-outline-legal"
					>View the Folio</a
				>
				<a href="/contact" class="btn-legal">Request Counsel</a>
			</div>
		</div>
	</section>
</div>
