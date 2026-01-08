<script lang="ts">
	import { onMount } from "svelte";

	const experience = [
		{
			title: "Software Engineer, Tech Lead",
			company: "Ford Motor Company Credit - Consumer Offers and Renewals",
			period: "Jan 2022 - Present",
			achievements: [
				"Migrated legacy Vue.js app to React.js, unifying tech stack and boosting scalability and productivity",
				"Built CI/CD pipelines with Google Cloud Build, automating deployments and improving release reliability",
				"Led cloud migration to GCP using Cloud Run, Postgres, and BigQuery for higher performance and lower cost",
				"Integrated Adobe Experience Manager with GraphQL APIs, streamlining content delivery workflows",
				"Enhanced observability with Cloud Monitoring, ContentSquare, and Splunk integrations",
				"Designed and deployed automated BigQuery-to-Postgres pipelines with Apache Beam on Dataflow, cutting data sync time and enhancing analytics reliability",
			],
		},
		{
			title: "Software Engineer",
			company: "Ford Motor Company Credit",
			period: "Jan 2021 – Dec 2021",
			achievements: [
				"Developed Vue.js front-end with Spring Boot microservices, improving modularity and scalability",
				"Built an ML-based next-vehicle recommendation app using Flask",
				"Cut API latency from ~5s to ~200ms through caching and ORM optimization",
				"Implemented WCAG-compliant E2E tests and optimized MySQL for high-volume environments",
				"Automated onboarding workflows with DevOps scripting to accelerate developer setup",
			],
		},
	];

	const skills = {
		Languages: ["Java", "Python", "JavaScript", "R", "C++", "Golang", "C"],
		Frameworks: [
			"React Native",
			"React",
			"Vue.js",
			"Java Spring Boot",
			"GraphQL",
		],
		DevOps: [
			"GitHub",
			"Jenkins",
			"Docker",
			"Google Cloud Build",
			"Cloud Run",
			"BigQuery",
		],
		Practices: ["Agile", "Paired Programming", "Test-Driven Development"],
	};

	let mounted = false;
	onMount(() => {
		mounted = true;
	});
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
				class="text-6xl sm:text-7xl md:text-8xl font-display font-black mb-4 text-mahogany tracking-tighter"
			>
				MOHAMMED HAMZA
			</h1>
			<div
				class="text-xl md:text-2xl text-brass font-display font-bold mb-8 uppercase tracking-[0.3em]"
			>
				Software Engineer & Counsel
			</div>
			<div class="w-32 h-1 bg-mahogany mx-auto mb-10"></div>
			<div
				class="text-lg text-mahogany/70 mb-12 font-serif italic max-w-2xl mx-auto leading-relaxed"
			>
				Specializing in the intersection of high-scale cloud
				architecture and legal precision. Currently building the future
				of automotive finance at Ford Credit.
			</div>
			<div class="flex flex-col sm:flex-row justify-center gap-6">
				<a href="/contact" class="btn-legal"> Request Brief </a>
				<a href="/projects" class="btn-outline-legal"> View Folio </a>
			</div>
		</div>
	</section>

	<!-- About Section: The Statement -->
	<section class="mb-40">
		<div class="flex flex-col md:flex-row gap-16 items-start">
			<div class="md:w-1/4 pt-2">
				<h2
					class="text-3xl font-display font-bold text-mahogany border-l-4 border-mahogany pl-6"
				>
					Statement of Intent
				</h2>
			</div>
			<div class="md:w-3/4 legal-folio p-10 md:p-14 bg-white/50">
				<div
					class="font-serif text-xl leading-relaxed space-y-6 text-ink"
				>
					<p>
						Accomplished Software Engineer and Technical Lead with a
						proven record of orchestrating complex cloud migrations
						and architecting resilient microservices. My approach
						combines the rigorous logic of computer science with the
						meticulous precision required for legal practice.
					</p>
					<p>
						Presently advancing technical initiatives while pursuing
						the transition into legal counsel, bridging the gap
						between innovative technology and regulatory excellence.
					</p>
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
				<div class="legal-folio p-10 md:p-14 group">
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
		<div class="legal-folio p-10 md:p-14 max-w-3xl mx-auto">
			<div
				class="flex flex-col md:flex-row md:items-baseline justify-between gap-4 mb-8"
			>
				<h3 class="text-3xl font-display font-bold text-mahogany">
					Wayne State University
				</h3>
				<span class="text-mahogany/60 font-display font-bold text-sm"
					>2017 – 2020</span
				>
			</div>
			<div
				class="text-2xl text-mahogany/90 font-display font-bold uppercase tracking-tight mb-4"
			>
				Bachelor of Science in Computer Science
			</div>
			<div class="text-lg text-mahogany/70 font-serif italic mb-2">
				Minor in Mathematics | Concentration in Data Science
			</div>
			<div
				class="text-mahogany/50 uppercase tracking-widest text-xs font-display"
			>
				Detroit, Michigan
			</div>
		</div>
	</section>

	<!-- Skills Section: Technical Competencies -->
	<section class="mb-40">
		<h2
			class="text-4xl font-display font-bold mb-16 text-mahogany text-center"
		>
			Technical Competencies
		</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
			{#each Object.entries(skills) as [category, items]}
				<div
					class="legal-folio p-10 flex flex-col items-center text-center"
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
</div>
