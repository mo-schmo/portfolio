<script lang="ts">
	import { page } from "$app/stores";
	import OracleChat from "$lib/components/oracle/OracleChat.svelte";

	// When launched from a project page (e.g. /oracles/tour?project=foo), anchor
	// the conversation to that exhibit so "this project" resolves correctly.
	$: projectSlug = $page.url.searchParams.get("project") ?? "";
	$: extraBody = projectSlug ? { project_slug: projectSlug } : {};

	const suggestions = [
		"What projects has Mohammed built with Go or Python?",
		"Tell me about the portfolio project and how it's built.",
		"Which works involve agentic AI, and what did he write about them?",
		"Walk me through his most technically ambitious project.",
	];

	$: anchoredSuggestions = projectSlug
		? [
				"Give me a tour of this project.",
				"What technologies does this project use?",
				"Are there related writings I should read?",
				...suggestions.slice(0, 1),
			]
		: suggestions;
</script>

<svelte:head>
	<title>Project Tour Guide - The Oracles</title>
	<meta
		name="description"
		content="Chat with the Project Tour Guide, a tool-using agent that fetches live project and blog records from the backend, showing every tool call on the wire."
	/>
</svelte:head>

<div class="container mx-auto px-4 py-20 max-w-6xl">
	<!-- Header -->
	<section class="text-center mb-12">
		<a
			href="/oracles"
			class="text-xs font-display tracking-[0.4em] text-brass uppercase hover:text-mahogany transition-colors"
		>
			&larr; The Chambers
		</a>
		<div
			class="text-xs font-display tracking-[0.4em] text-brass uppercase mt-6 mb-3"
		>
			Oracle III &middot; Tool-Using Agent
		</div>
		<h1
			class="text-5xl md:text-7xl font-display font-black mb-4 text-mahogany tracking-tighter uppercase"
		>
			Project Tour Guide
		</h1>
		<div class="w-24 h-1 bg-mahogany mx-auto mb-6"></div>
		<p
			class="text-lg text-mahogany/80 font-serif italic max-w-2xl mx-auto leading-relaxed"
		>
			A guide who walks the halls of the works - retrieving the relevant
			records as you ask, with every tool call shown on the wire.
		</p>
		{#if projectSlug}
			<p class="mt-4 text-sm font-display tracking-[0.2em] uppercase text-brass">
				Anchored to exhibit: {projectSlug}
			</p>
		{/if}
	</section>

	<!-- Layout: Chat + Sidebar -->
	<section class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
		<div class="lg:col-span-2 oracle-illumination">
			{#key projectSlug}
				<OracleChat
					bot="tour"
					endpoint="/agents/tour/chat"
					title="Project Tour Guide"
					subtitle="Calls live tools against the archive. Watch the wire."
					placeholder="Ask about a project, a technology, or related writing..."
					initialPrompts={anchoredSuggestions}
					{extraBody}
				/>
			{/key}
		</div>

		<aside class="space-y-6">
			<div class="legal-folio bg-white/60 p-8">
				<div
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-3"
				>
					On the Method
				</div>
				<h2
					class="text-lg font-display font-black text-mahogany uppercase tracking-tight mb-4"
				>
					How the Guide Reasons
				</h2>
				<ol class="space-y-3 font-serif text-sm text-ink/80 leading-relaxed">
					<li>
						<span class="font-bold text-mahogany">i.</span> The guide
						is given a set of read-only tools over the Go backend.
					</li>
					<li>
						<span class="font-bold text-mahogany">ii.</span> As it
						answers, it decides when to call
						<span class="font-mono text-xs">get_project</span> or
						<span class="font-mono text-xs">list_related_blog</span>.
					</li>
					<li>
						<span class="font-bold text-mahogany">iii.</span> Each
						invocation is streamed to the wire above, with its
						arguments and a summary of the result.
					</li>
					<li>
						<span class="font-bold text-mahogany">iv.</span> The
						guide then grounds its reply in the records it pulled.
					</li>
				</ol>
			</div>

			<div class="legal-folio bg-parchment/70 p-8">
				<div
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-3"
				>
					Instruments
				</div>
				<div class="flex flex-wrap gap-2">
					{#each ["get_project", "list_related_blog"] as tool}
						<span
							class="px-3 py-1 bg-mahogany/5 border border-mahogany/15 text-[10px] font-mono uppercase tracking-widest text-mahogany/70"
						>
							{tool}
						</span>
					{/each}
				</div>
				<p
					class="mt-4 font-serif text-sm text-ink/70 italic leading-relaxed"
				>
					Expand "Tools on the Wire" in any answer to inspect the
					exact calls the guide made and what came back.
				</p>
			</div>
		</aside>
	</section>
</div>
