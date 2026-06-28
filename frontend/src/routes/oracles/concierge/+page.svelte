<script lang="ts">
	import OracleChat from "$lib/components/oracle/OracleChat.svelte";

	const suggestions = [
		"What is Mohammed's experience with cloud migrations?",
		"Which projects use Golang or Python?",
		"What does he say about agentic AI in his recent writing?",
		"Walk me through his transition from legal assistant to tech lead.",
	];
</script>

<svelte:head>
	<title>Portfolio Concierge - The Oracles</title>
	<meta
		name="description"
		content="Chat with the Portfolio Concierge, a RAG agent that has read Mohammed's resume, projects, and blog posts and answers with citations."
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
			Oracle I &middot; Retrieval-Augmented Counsel
		</div>
		<h1
			class="text-5xl md:text-7xl font-display font-black mb-4 text-mahogany tracking-tighter uppercase"
		>
			Portfolio Concierge
		</h1>
		<div class="w-24 h-1 bg-mahogany mx-auto mb-6"></div>
		<p
			class="text-lg text-mahogany/80 font-serif italic max-w-2xl mx-auto leading-relaxed"
		>
			This counsel has read every page of the folio - resume, projects,
			and writings - and answers with citations to the record.
		</p>
	</section>

	<!-- Layout: Chat + Sidebar -->
	<section class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
		<div class="lg:col-span-2 oracle-illumination">
			<OracleChat
				bot="concierge"
				endpoint="/agents/concierge/chat"
				title="Portfolio Concierge"
				subtitle="Grounded in the archive. Every claim is cited."
				placeholder="Ask about an experience, project, or blog post..."
				initialPrompts={suggestions}
			/>
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
					How the Counsel Reasons
				</h2>
				<ol class="space-y-3 font-serif text-sm text-ink/80 leading-relaxed">
					<li>
						<span class="font-bold text-mahogany">i.</span> The
						archive is embedded once at startup using a local
						<span class="font-mono text-xs">BAAI/bge-small-en-v1.5</span>
						model.
					</li>
					<li>
						<span class="font-bold text-mahogany">ii.</span> Each
						question retrieves the most relevant chunks by cosine
						similarity.
					</li>
					<li>
						<span class="font-bold text-mahogany">iii.</span> The
						model is asked to answer only from those chunks, citing
						sources inline.
					</li>
					<li>
						<span class="font-bold text-mahogany">iv.</span>{" "}
						Citations render as chips beneath the answer, linking
						back to the cited page.
					</li>
				</ol>
			</div>

			<div class="legal-folio bg-parchment/70 p-8">
				<div
					class="text-[10px] font-display tracking-[0.3em] uppercase text-brass mb-3"
				>
					Notice
				</div>
				<p class="font-serif text-sm text-ink/70 italic leading-relaxed">
					The Concierge answers only from the archive. If a question
					ventures outside what has been recorded, the counsel will
					say so plainly.
				</p>
			</div>
		</aside>
	</section>
</div>
