<script lang="ts">
	import { onMount } from "svelte";

	export let data;
	$: posts = data.posts || [];

	function formatDate(dateString: string): string {
		const date = new Date(dateString);
		return date.toLocaleDateString("en-US", {
			year: "numeric",
			month: "long",
			day: "numeric",
		});
	}
</script>

<svelte:head>
	<title>Blog - Mohammed Hamza</title>
</svelte:head>

<div class="container mx-auto px-4 py-28 max-w-6xl">
	<div class="text-center mb-24">
		<h1
			class="text-6xl md:text-8xl font-display font-black mb-6 text-mahogany tracking-tighter"
		>
			The Briefing
		</h1>
		<div class="w-24 h-1 bg-mahogany mx-auto mb-8"></div>
		<p class="text-xl text-mahogany/70 max-w-2xl mx-auto font-serif italic">
			Dispatches from the intersection of technology and law.
		</p>
	</div>

	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
		{#each posts as post}
			<a
				href="/blog/{post.slug}"
				class="legal-folio p-10 flex flex-col group bg-white/50"
			>
				<div
					class="text-brass font-display font-bold text-xs mb-6 tracking-[0.2em] uppercase border-b border-brass/20 pb-2"
				>
					{formatDate(post.publishedAt)}
				</div>
				<h2
					class="text-2xl font-display font-bold text-mahogany mb-4 group-hover:text-brass transition-colors line-clamp-2"
				>
					{post.title}
				</h2>
				<p
					class="mb-8 flex-grow text-ink/80 font-serif leading-relaxed line-clamp-3 italic"
				>
					{post.excerpt}
				</p>
				<div
					class="flex items-center text-mahogany font-display font-bold uppercase tracking-widest text-xs group-hover:translate-x-1 transition-transform"
				>
					Read Full Dispatch
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-4 w-4 ml-2"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M14 5l7 7m0 0l-7 7m7-7H3"
						/>
					</svg>
				</div>
			</a>
		{/each}
	</div>
</div>
