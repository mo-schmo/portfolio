<script lang="ts">
	import { resume } from "$lib/content/resume";

	const { experience, skills, education, statement, name, title, tagline } =
		resume;
</script>

<svelte:head>
	<title>Mohammed Hamza - Software Engineer</title>
</svelte:head>

<div class="container mx-auto px-4 py-28 max-w-5xl">
	<!-- Hero Section: The Legal Header -->
	<section
		class="text-center mb-40 border-b-4 border-double border-mahogany pb-20"
	>
		<div class="max-w-4xl mx-auto">
			<div class="mb-8 flex justify-center">
				<div
					class="w-16 h-16 border-2 border-mahogany rounded-full flex items-center justify-center font-display font-bold text-2xl text-mahogany"
				>
					MH
				</div>
			</div>
			<h1
				class="text-6xl sm:text-7xl md:text-8xl font-display font-black mb-4 text-mahogany tracking-tighter uppercase"
			>
				{name}
			</h1>
			<div
				class="text-xl md:text-2xl text-brass font-display font-bold mb-8 uppercase tracking-[0.3em]"
			>
				{title}
			</div>
			<div class="w-32 h-1 bg-mahogany mx-auto mb-10"></div>
			<div
				class="text-lg text-mahogany/70 mb-12 font-serif italic max-w-2xl mx-auto leading-relaxed"
			>
				{tagline}
			</div>
			<div
				class="flex flex-col sm:flex-row justify-center items-center gap-6"
			>
				<a href="/contact" class="btn-legal"> Request Brief </a>
				<a href="/projects" class="btn-outline-legal"> View Folio </a>
				<a href="/oracles" class="btn-illuminated">
					Consult the Oracles
				</a>
			</div>
		</div>
	</section>

	<!-- About Section: The Statement -->
	<section class="mb-40">
		<div class="flex flex-col md:flex-row gap-16 items-start">
			<div class="md:w-1/4 pt-2">
				<div
					class="text-xs font-display tracking-[0.4em] text-brass uppercase mb-3"
				>
					Article I
				</div>
				<h2
					class="text-3xl font-display font-bold text-mahogany border-l-4 border-mahogany pl-6"
				>
					Statement of Intent
				</h2>
			</div>
			<div class="md:w-3/4 legal-folio ink-bloom p-10 md:p-14 bg-white/50">
				<div
					class="font-serif text-xl leading-relaxed space-y-6 text-ink"
				>
					{#each statement as paragraph}
						<p>{paragraph}</p>
					{/each}
				</div>
			</div>
		</div>
	</section>

	<!-- Experience Section: Professional Record -->
	<section class="mb-40">
		<h2
			class="text-4xl font-display font-bold mb-16 text-mahogany text-center"
		>
			Professional Record
		</h2>
		<div class="space-y-16">
			{#each experience as exp}
				<div class="legal-folio ink-bloom p-10 md:p-14 group">
					<div class="mb-10">
						<div
							class="flex flex-col md:flex-row md:items-baseline justify-between gap-4 mb-6"
						>
							<h3
								class="text-3xl font-display font-bold text-mahogany uppercase tracking-tight"
							>
								{exp.title}
							</h3>
							<span
								class="text-brass font-display font-bold uppercase tracking-widest text-sm border-b-2 border-brass/30 pb-1"
							>
								{exp.period}
							</span>
						</div>
						<div
							class="text-xl text-mahogany/80 font-display font-black uppercase tracking-wider"
						>
							{exp.company}
						</div>
					</div>
					<ul class="space-y-6">
						{#each exp.achievements as achievement}
							<li class="flex items-start">
								<span class="text-mahogany mr-4 mt-1">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="h-5 w-5"
										viewBox="0 0 20 20"
										fill="currentColor"
									>
										<path
											fill-rule="evenodd"
											d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
											clip-rule="evenodd"
										/>
									</svg>
								</span>
								<span
									class="text-lg text-ink/90 leading-relaxed font-serif"
									>{achievement}</span
								>
							</li>
						{/each}
					</ul>
				</div>
			{/each}
		</div>
	</section>

	<!-- Education Section: Academic Credentials -->
	<section class="mb-40">
		<h2
			class="text-4xl font-display font-bold mb-16 text-mahogany text-center"
		>
			Academic Credentials
		</h2>
		<div class="space-y-12 max-w-3xl mx-auto">
			{#each education as edu}
				<div class="legal-folio ink-bloom p-10 md:p-14">
					<div
						class="flex flex-col md:flex-row md:items-baseline justify-between gap-4 mb-8"
					>
						<h3
							class="text-3xl font-display font-bold text-mahogany"
						>
							{edu.institution}
						</h3>
						<span
							class="text-mahogany/60 font-display font-bold text-sm"
						>
							{edu.period}
						</span>
					</div>
					<div
						class="text-2xl text-mahogany/90 font-display font-bold uppercase tracking-tight mb-4"
					>
						{edu.degree}
					</div>
					<div class="text-lg text-mahogany/70 font-serif italic mb-2">
						{edu.concentration}
					</div>
					<div
						class="text-mahogany/50 uppercase tracking-widest text-xs font-display"
					>
						{edu.location}
					</div>
				</div>
			{/each}
		</div>
	</section>

	<!-- Skills Section: Technical Competencies -->
	<section class="mb-40">
		<h2
			class="text-4xl font-display font-bold mb-16 text-mahogany text-center"
		>
			Technical Competencies
		</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{#each Object.entries(skills) as [category, items]}
				<div
					class="legal-folio ink-bloom p-10 flex flex-col items-center text-center"
				>
					<h3
						class="text-xl font-display font-black text-mahogany mb-8 border-b-2 border-mahogany pb-4 w-full uppercase tracking-tighter"
					>
						{category}
					</h3>
					<ul class="space-y-4 w-full">
						{#each items as item}
							<li class="text-lg text-ink font-serif italic">
								{item}
							</li>
						{/each}
					</ul>
				</div>
			{/each}
		</div>
	</section>

	<!-- Counsel Chamber: Oracle Preview -->
	<section class="mb-20">
		<div class="text-center mb-16">
			<div
				class="text-xs font-display tracking-[0.4em] text-brass uppercase mb-4"
			>
				Chambers of Counsel
			</div>
			<h2
				class="text-4xl md:text-5xl font-display font-black text-mahogany tracking-tighter"
			>
				Consult the Oracles
			</h2>
			<div class="w-24 h-1 bg-brass mx-auto mt-6 mb-6"></div>
			<p
				class="text-lg text-mahogany/70 font-serif italic max-w-2xl mx-auto"
			>
				Four agentic counsels stand at the ready &mdash; reading the
				archive, drafting compliance, guiding tours, and parsing the
				fine print.
			</p>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
			<a
				href="/oracles"
				class="legal-folio p-10 group oracle-illumination ink-bloom"
			>
				<div
					class="text-xs font-display tracking-[0.3em] text-brass uppercase mb-3"
				>
					Oracle I &middot; Retrieval
				</div>
				<h3
					class="text-2xl font-display font-black text-mahogany mb-3 uppercase tracking-tight"
				>
					Portfolio Concierge
				</h3>
				<p class="text-ink/80 font-serif italic leading-relaxed">
					An informed counsel that has read every page of this folio.
					Ask anything about the work, the writing, or the record.
				</p>
			</a>

			<a
				href="/oracles"
				class="legal-folio p-10 group oracle-illumination ink-bloom"
			>
				<div
					class="text-xs font-display tracking-[0.3em] text-brass uppercase mb-3"
				>
					Oracle II &middot; Multi-Agent
				</div>
				<h3
					class="text-2xl font-display font-black text-mahogany mb-3 uppercase tracking-tight"
				>
					Patent Compliance Bench
				</h3>
				<p class="text-ink/80 font-serif italic leading-relaxed">
					A bench of three: a Drafter, a Reviewer, and a Revisor. They
					confer in chambers and return a compliance memorandum.
				</p>
			</a>

			<a
				href="/oracles"
				class="legal-folio p-10 group oracle-illumination ink-bloom"
			>
				<div
					class="text-xs font-display tracking-[0.3em] text-brass uppercase mb-3"
				>
					Oracle III &middot; Tool Use
				</div>
				<h3
					class="text-2xl font-display font-black text-mahogany mb-3 uppercase tracking-tight"
				>
					Project Tour Guide
				</h3>
				<p class="text-ink/80 font-serif italic leading-relaxed">
					A guide who walks the halls of the works, retrieving the
					relevant records as you ask &mdash; with every tool call
					shown on the wire.
				</p>
			</a>

			<a
				href="/oracles"
				class="legal-folio p-10 group oracle-illumination ink-bloom"
			>
				<div
					class="text-xs font-display tracking-[0.3em] text-brass uppercase mb-3"
				>
					Oracle IV &middot; Structured Output
				</div>
				<h3
					class="text-2xl font-display font-black text-mahogany mb-3 uppercase tracking-tight"
				>
					Clause Explainer
				</h3>
				<p class="text-ink/80 font-serif italic leading-relaxed">
					Paste a contract clause; receive a memorandum of counsel
					&mdash; plain English, obligations enumerated, risks
					flagged.
				</p>
			</a>
		</div>

		<div class="text-center">
			<a href="/oracles" class="btn-outline-legal">
				Enter the Chambers
			</a>
		</div>
	</section>
</div>
