<script lang="ts">
	import { onMount } from "svelte";
	import { resume } from "$lib/content/resume";
	import { ORACLES_ENABLED } from "$lib/config/features";

	const { experience, skills, education, statement, name, title, tagline } =
		resume;

	// Masthead: split first/last name for two-line setting on wide viewports.
	const [firstName, ...rest] = name.split(" ");
	const lastName = rest.join(" ");

	const currentYear = new Date().getFullYear();

	const oraclePreviews = [
		{
			roman: "II",
			discipline: "Multi-Agent",
			title: "Patent Compliance Bench",
			teaser:
				"A Drafter, a Reviewer, and a Revisor confer in chambers and return a compliance memorandum.",
			href: "/oracles/patent",
		},
		{
			roman: "III",
			discipline: "Tool Use",
			title: "Project Tour Guide",
			teaser:
				"A guide who walks the halls of the works, retrieving records as you ask — every tool call shown on the wire.",
			href: "/oracles/tour",
		},
		{
			roman: "IV",
			discipline: "Structured Output",
			title: "Clause Explainer",
			teaser:
				"Paste a clause; receive plain English, enumerated obligations, and flagged risks.",
			href: "/oracles/clause",
		},
	];

	let pageEl: HTMLElement | null = null;

	onMount(() => {
		if (!pageEl) return;
		const rules = pageEl.querySelectorAll<HTMLElement>(".rule-reveal");
		if (!rules.length || typeof IntersectionObserver === "undefined") return;
		const io = new IntersectionObserver(
			(entries) => {
				for (const entry of entries) {
					if (entry.isIntersecting) {
						entry.target.classList.add("is-visible");
						io.unobserve(entry.target);
					}
				}
			},
			{ rootMargin: "-10% 0px -10% 0px", threshold: 0.01 },
		);
		rules.forEach((r) => io.observe(r));
		return () => io.disconnect();
	});
</script>

<svelte:head>
	<title>Mohammed Hamza — Software Engineer</title>
</svelte:head>

<article bind:this={pageEl} class="masthead-page mx-auto px-6 max-w-6xl">
	<!-- ============================================================
		 HERO — Masthead cover
		 ============================================================ -->
	<section class="hero pt-20 pb-16 md:pt-28 md:pb-24">
		<div class="grid grid-cols-12 gap-x-6 gap-y-10 items-start">
			<!-- Masthead block -->
			<header class="col-span-12 md:col-span-8">
				<div class="eyebrow stagger-up" style="animation-delay: 0ms;">
					Vol. I &middot; Folio of Mohammed Hamza &middot; MMXXVI
				</div>

				<h1
					class="masthead-name mt-6 stagger-up"
					style="animation-delay: 80ms;"
				>
					<span class="block">{firstName}</span>
					{#if lastName}
						<span class="block">{lastName}</span>
					{/if}
				</h1>

				<p
					class="masthead-subtitle mt-7 stagger-up"
					style="animation-delay: 160ms;"
				>
					{title} &mdash; building tools that read, draft, and reason.
				</p>

				<p
					class="masthead-tagline mt-6 max-w-2xl stagger-up"
					style="animation-delay: 220ms;"
				>
					{tagline}
				</p>

				<nav
					class="hero-cta mt-10 stagger-up"
					style="animation-delay: 300ms;"
					aria-label="Primary actions"
				>
					<a href="/contact" class="btn-legal">Request Brief</a>
					<a href="/projects" class="cta-link">
						<span>Read the Folio</span>
						<span class="cta-arrow" aria-hidden="true">&rarr;</span>
					</a>
					{#if ORACLES_ENABLED}
						<a href="/oracles" class="cta-link cta-link--accent">
							<span>Consult the Oracles</span>
							<span class="cta-arrow" aria-hidden="true"
								>&#8599;</span
							>
						</a>
					{/if}
				</nav>
			</header>

			<!-- Colophon / dateline marginalia -->
			<aside
				class="col-span-12 md:col-span-4 md:pt-3 dateline stagger-up"
				style="animation-delay: 360ms;"
				aria-label="Colophon"
			>
				<span class="hairline-soft mb-3" aria-hidden="true"></span>
				<dl class="marginalia grid grid-cols-[auto,1fr] gap-x-6 gap-y-1">
					<dt>Issue</dt>
					<dd>No. {currentYear - 2019}</dd>
					<dt>Est.</dt>
					<dd>MMXXI</dd>
					<dt>Loc.</dt>
					<dd>Detroit / Remote</dd>
					<dt>Focus</dt>
					<dd>AI &middot; Cloud &middot; Legal</dd>
					<dt>Status</dt>
					<dd>
						<span class="status-dot" aria-hidden="true"></span>
						Available
					</dd>
				</dl>
				<span class="hairline-soft mt-3" aria-hidden="true"></span>
			</aside>
		</div>

		<span class="hairline rule-reveal mt-16" aria-hidden="true"></span>
	</section>

	<!-- ============================================================
		 ARTICLE I — Statement of Intent
		 ============================================================ -->
	<section class="mb-28 md:mb-32">
		<div class="grid grid-cols-12 gap-x-6">
			<aside class="col-span-12 md:col-span-3 mb-6 md:mb-0 md:pt-2">
				<div class="eyebrow">Article I</div>
				<h2 class="article-label mt-2">Statement<br />of Intent</h2>
			</aside>

			<div class="col-span-12 md:col-span-9">
				<div class="dropcap statement-body">
					{#each statement as paragraph, i}
						<p class:mt-7={i > 0}>{paragraph}</p>
					{/each}
				</div>
			</div>
		</div>
	</section>

	<!-- ============================================================
		 ARTICLE II — Professional Record
		 ============================================================ -->
	<section class="mb-32 md:mb-36">
		<header class="section-head mb-12">
			<div class="eyebrow">Article II</div>
			<h2 class="section-title mt-2">Professional Record</h2>
			<span class="hairline rule-reveal mt-6" aria-hidden="true"></span>
		</header>

		<ol class="experience-list">
			{#each experience as exp}
				<li class="experience-entry grid grid-cols-12 gap-x-6 gap-y-4">
					<div class="col-span-12 md:col-span-3 md:pt-1">
						<div class="marginalia">{exp.period}</div>
					</div>
					<div class="col-span-12 md:col-span-9">
						<div class="kicker">{exp.company}</div>
						<h3 class="entry-title mt-2">{exp.title}</h3>
						<ul class="achievement-list mt-6 space-y-3">
							{#each exp.achievements as achievement, idx}
								<li class="flex gap-4">
									<span class="figured-num pt-1.5"
										>{(idx + 1)
											.toString()
											.padStart(2, "0")}</span
									>
									<span class="achievement-body"
										>{achievement}</span
									>
								</li>
							{/each}
						</ul>
					</div>
				</li>
			{/each}
		</ol>
	</section>

	<!-- ============================================================
		 ARTICLE III — Academic Credentials
		 ============================================================ -->
	<section class="mb-28 md:mb-32">
		<header class="section-head mb-10">
			<div class="eyebrow">Article III</div>
			<h2 class="section-title mt-2">Academic Credentials</h2>
			<span class="hairline rule-reveal mt-6" aria-hidden="true"></span>
		</header>

		<div class="grid grid-cols-12 gap-x-6 gap-y-10">
			{#each education as edu}
				<div class="col-span-12 md:col-span-7">
					<h3 class="entry-title">{edu.institution}</h3>
					<div class="kicker mt-1">{edu.degree}</div>
					<p class="mt-3 text-mahogany/70 italic">
						{edu.concentration}
					</p>
				</div>
				<div class="col-span-12 md:col-span-5 md:pt-2">
					<dl class="marginalia grid grid-cols-[auto,1fr] gap-x-6 gap-y-1">
						<dt>Period</dt>
						<dd>{edu.period}</dd>
						<dt>Locus</dt>
						<dd>{edu.location}</dd>
					</dl>
				</div>
			{/each}
		</div>
	</section>

	<!-- ============================================================
		 ARTICLE IV — Technical Competencies
		 ============================================================ -->
	<section class="mb-32 md:mb-36">
		<header class="section-head mb-10">
			<div class="eyebrow">Article IV</div>
			<h2 class="section-title mt-2">Technical Competencies</h2>
			<span class="hairline rule-reveal mt-6" aria-hidden="true"></span>
		</header>

		<dl class="competencies">
			{#each Object.entries(skills) as [category, items], i}
				<div
					class="competency-row grid grid-cols-12 gap-x-6 py-7"
					class:competency-row--alt={i % 2 === 1}
				>
					<dt class="col-span-12 md:col-span-3 eyebrow self-start md:pt-2">
						{category}
					</dt>
					<dd class="col-span-12 md:col-span-9 competency-items">
						{items.join(",  ")}
					</dd>
				</div>
			{/each}
		</dl>
	</section>

	<!-- ============================================================
		 CHAMBERS OF COUNSEL — Oracle preview (feature-flagged)
		 ============================================================ -->
	{#if ORACLES_ENABLED}
	<section class="mb-24 md:mb-28">
		<header class="section-head mb-12">
			<div class="eyebrow">Chambers of Counsel</div>
			<h2 class="section-title mt-2">Consult the Oracles</h2>
			<p class="section-deck mt-4 max-w-2xl">
				Four agentic counsels stand at the ready &mdash; reading the
				archive, drafting compliance, guiding tours, and parsing the
				fine print.
			</p>
			<span class="hairline rule-reveal mt-8" aria-hidden="true"></span>
		</header>

		<div class="grid grid-cols-12 gap-x-6 gap-y-12">
			<!-- Featured Oracle I -->
			<a
				href="/oracles/concierge"
				class="featured-oracle col-span-12 md:col-span-7 group"
			>
				<div class="featured-roman">I</div>
				<div class="eyebrow mt-3">Oracle I &middot; Retrieval</div>
				<h3 class="featured-title mt-3">Portfolio Concierge</h3>
				<p class="featured-deck mt-5">
					An informed counsel that has read every page of this folio
					&mdash; the resume, the projects, the writing. Ask
					anything about the work, the writing, or the record, and
					receive answers grounded in the source with inline
					citations back to the page they came from.
				</p>
				<div class="featured-cta mt-7">
					<span>Enter chambers</span>
					<span class="cta-arrow" aria-hidden="true">&rarr;</span>
				</div>
			</a>

			<!-- Oracles II - IV in a stacked list -->
			<ul class="col-span-12 md:col-span-5 oracle-list">
				{#each oraclePreviews as oracle, i}
					<li class="oracle-list-item">
						{#if i > 0}
							<span class="hairline-soft mb-7" aria-hidden="true"
							></span>
						{/if}
						<a href={oracle.href} class="oracle-list-link group">
							<div class="flex items-baseline gap-4">
								<span class="oracle-roman">{oracle.roman}</span>
								<span class="eyebrow"
									>Oracle {oracle.roman} &middot;
									{oracle.discipline}</span
								>
							</div>
							<h4 class="oracle-list-title mt-2">
								{oracle.title}
							</h4>
							<p class="oracle-list-teaser mt-2">
								{oracle.teaser}
							</p>
						</a>
					</li>
				{/each}
			</ul>
		</div>
	</section>
	{/if}

	<span class="hairline mb-20" aria-hidden="true"></span>
</article>

<style>
	/* ============================================================
	   Local masthead styles. Generic editorial tokens (.eyebrow,
	   .marginalia, .hairline, .dropcap, .kicker, .figured-num)
	   live in app.css so other pages can reuse them later.
	   ============================================================ */

	/* ---------- HERO ---------- */

	.masthead-name {
		font-family: 'Playfair Display', serif;
		font-weight: 600;
		font-size: var(--step-7);
		line-height: 0.88;
		letter-spacing: -0.03em;
		color: var(--mahogany);
	}

	.masthead-name :global(span:nth-child(2)) {
		color: var(--mahogany);
		font-style: italic;
		font-weight: 500;
		margin-left: 0.5ch;
	}

	.masthead-subtitle {
		font-family: 'Newsreader', 'PT Serif', serif;
		font-style: italic;
		font-weight: 400;
		font-size: var(--step-2);
		color: color-mix(in oklch, var(--mahogany) 85%, transparent);
		line-height: 1.35;
		max-width: 36ch;
	}

	.masthead-tagline {
		font-family: 'Newsreader', 'PT Serif', serif;
		font-size: var(--step-1);
		line-height: 1.55;
		color: color-mix(in oklch, var(--mahogany) 65%, transparent);
	}

	.hero-cta {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 1.25rem 2rem;
	}

	/* Link-style CTA, replacing the second boxed button row */
	.cta-link {
		display: inline-flex;
		align-items: baseline;
		gap: 0.5ch;
		font-family: 'Playfair Display', serif;
		font-weight: 500;
		font-size: var(--step-0);
		color: var(--mahogany);
		position: relative;
		padding-bottom: 0.15em;
		transition: color 200ms ease-out;
	}

	.cta-link::after {
		content: '';
		position: absolute;
		left: 0;
		right: 0;
		bottom: 0;
		height: 1px;
		background: var(--rule);
		transform: scaleX(1);
		transform-origin: left center;
		transition: background 200ms ease-out, transform 240ms cubic-bezier(0.2, 0.7, 0.2, 1);
	}

	.cta-link:hover::after {
		background: var(--mahogany);
	}

	.cta-link .cta-arrow {
		transition: transform 240ms cubic-bezier(0.2, 0.7, 0.2, 1);
	}

	.cta-link:hover .cta-arrow {
		transform: translateX(3px) translateY(-1px);
	}

	.cta-link--accent {
		color: var(--brass);
	}

	.cta-link--accent::after {
		background: color-mix(in oklch, var(--brass) 45%, transparent);
	}

	.cta-link--accent:hover::after {
		background: var(--brass);
	}

	.cta-link--accent:hover {
		color: var(--mahogany);
	}

	/* Colophon / dateline */
	.dateline :global(dt) {
		color: color-mix(in oklch, var(--mahogany) 50%, transparent);
	}

	.dateline :global(dd) {
		color: color-mix(in oklch, var(--mahogany) 80%, transparent);
		font-weight: 500;
	}

	.status-dot {
		display: inline-block;
		width: 6px;
		height: 6px;
		border-radius: 50%;
		background: oklch(0.58 0.16 145);
		margin-right: 0.5ch;
		vertical-align: 0.12em;
		box-shadow: 0 0 0 2px color-mix(in oklch, oklch(0.58 0.16 145) 25%, transparent);
	}

	/* ---------- ARTICLE / SECTION HEADS ---------- */

	.article-label {
		font-family: 'Playfair Display', serif;
		font-weight: 500;
		font-size: var(--step-3);
		line-height: 1;
		color: var(--mahogany);
		letter-spacing: -0.015em;
	}

	.section-title {
		font-family: 'Playfair Display', serif;
		font-weight: 600;
		font-size: var(--step-5);
		line-height: 1;
		color: var(--mahogany);
		letter-spacing: -0.02em;
	}

	.section-deck {
		font-family: 'Newsreader', 'PT Serif', serif;
		font-style: italic;
		font-size: var(--step-1);
		color: color-mix(in oklch, var(--mahogany) 70%, transparent);
		line-height: 1.5;
	}

	/* ---------- STATEMENT ---------- */

	.statement-body {
		font-family: 'Newsreader', 'PT Serif', serif;
		font-size: var(--step-2);
		line-height: 1.55;
		color: var(--ink);
		max-width: 62ch;
		font-weight: 400;
	}

	/* ---------- EXPERIENCE / EDUCATION ENTRIES ---------- */

	.entry-title {
		font-family: 'Playfair Display', serif;
		font-weight: 600;
		font-size: var(--step-3);
		line-height: 1.1;
		color: var(--mahogany);
		letter-spacing: -0.015em;
	}

	.achievement-body {
		font-family: 'Newsreader', 'PT Serif', serif;
		font-size: var(--step-1);
		line-height: 1.55;
		color: color-mix(in oklch, var(--ink) 92%, transparent);
	}

	/* Experience list — entries separated by hairlines */
	.experience-list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.experience-entry {
		padding-bottom: 2.5rem;
		margin-bottom: 2.5rem;
		border-bottom: 1px solid var(--rule-soft);
	}

	.experience-entry:last-child {
		padding-bottom: 0;
		margin-bottom: 0;
		border-bottom: 0;
	}

	.achievement-list {
		list-style: none;
		padding: 0;
		margin-top: 1.5rem;
	}

	/* ---------- COMPETENCIES ---------- */

	.competencies {
		border-top: 1px solid var(--rule);
	}

	.competency-row {
		border-bottom: 1px solid var(--rule);
	}

	.competency-row--alt {
		background: color-mix(in oklch, var(--parchment-dark) 35%, transparent);
		margin-left: -1rem;
		margin-right: -1rem;
		padding-left: 1rem;
		padding-right: 1rem;
	}

	.competency-items {
		font-family: 'Newsreader', 'PT Serif', serif;
		font-size: var(--step-1);
		line-height: 1.6;
		color: color-mix(in oklch, var(--ink) 92%, transparent);
		font-feature-settings: 'liga' 1, 'kern' 1;
	}

	/* ---------- ORACLES ---------- */

	.featured-oracle {
		display: block;
		padding: 2rem 1.25rem 2.25rem 1.25rem;
		position: relative;
		transition: color 240ms ease-out;
	}

	.featured-oracle::before {
		content: '';
		position: absolute;
		left: 0;
		top: 0;
		bottom: 0;
		width: 1px;
		background: var(--rule);
		transition: background 240ms ease-out, width 240ms ease-out;
	}

	.featured-oracle:hover::before {
		background: var(--brass);
		width: 2px;
	}

	.featured-roman {
		font-family: 'Playfair Display', serif;
		font-style: italic;
		font-weight: 500;
		font-size: var(--step-6);
		line-height: 0.85;
		color: color-mix(in oklch, var(--brass) 70%, transparent);
		letter-spacing: -0.02em;
	}

	.featured-title {
		font-family: 'Playfair Display', serif;
		font-weight: 600;
		font-size: var(--step-4);
		line-height: 1.05;
		color: var(--mahogany);
		letter-spacing: -0.02em;
	}

	.featured-deck {
		font-family: 'Newsreader', 'PT Serif', serif;
		font-size: var(--step-1);
		line-height: 1.55;
		color: color-mix(in oklch, var(--ink) 88%, transparent);
		max-width: 48ch;
	}

	.featured-cta {
		display: inline-flex;
		align-items: baseline;
		gap: 0.5ch;
		font-family: 'Playfair Display', serif;
		font-weight: 500;
		color: var(--brass);
		font-size: var(--step-0);
		letter-spacing: 0.01em;
		border-bottom: 1px solid color-mix(in oklch, var(--brass) 45%, transparent);
		padding-bottom: 0.15em;
		transition: color 200ms ease-out, border-color 200ms ease-out;
	}

	.featured-oracle:hover .featured-cta {
		color: var(--mahogany);
		border-bottom-color: var(--mahogany);
	}

	.featured-oracle:hover .cta-arrow {
		transform: translateX(3px);
	}

	.featured-oracle .cta-arrow {
		transition: transform 240ms cubic-bezier(0.2, 0.7, 0.2, 1);
	}

	/* Oracle list (II - IV) */
	.oracle-list {
		display: flex;
		flex-direction: column;
		gap: 1.75rem;
	}

	.oracle-list-item {
		display: flex;
		flex-direction: column;
	}

	.oracle-list-link {
		display: block;
		position: relative;
		transition: transform 240ms cubic-bezier(0.2, 0.7, 0.2, 1);
	}

	.oracle-list-link:hover {
		transform: translateX(4px);
	}

	.oracle-roman {
		font-family: 'Playfair Display', serif;
		font-style: italic;
		font-weight: 500;
		color: var(--brass);
		font-size: var(--step-1);
	}

	.oracle-list-title {
		font-family: 'Playfair Display', serif;
		font-weight: 600;
		font-size: var(--step-2);
		line-height: 1.1;
		color: var(--mahogany);
		letter-spacing: -0.01em;
	}

	.oracle-list-teaser {
		font-family: 'Newsreader', 'PT Serif', serif;
		font-size: var(--step-0);
		line-height: 1.5;
		color: color-mix(in oklch, var(--ink) 75%, transparent);
		max-width: 36ch;
	}

	/* ---------- MOTION REDUCED ---------- */

	@media (prefers-reduced-motion: reduce) {
		.cta-link .cta-arrow,
		.featured-oracle:hover .cta-arrow,
		.oracle-list-link {
			transition: none !important;
			transform: none !important;
		}
	}
</style>
