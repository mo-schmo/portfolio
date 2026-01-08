<script lang="ts">
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";

	export let data;
	$: post = data.post;

	function formatDate(dateString: string): string {
		const date = new Date(dateString);
		return date.toLocaleDateString("en-US", {
			year: "numeric",
			month: "long",
			day: "numeric",
		});
	}

	function renderMarkdown(text: string): string {
		// Simple markdown to HTML conversion for basic formatting
		let html = text;

		// Headers (must be processed first, before paragraphs)
		html = html.replace(
			/^### (.*$)/gim,
			'<h3 class="text-2xl font-display font-bold text-mahogany mb-4 mt-8">$1</h3>',
		);
		html = html.replace(
			/^## (.*$)/gim,
			'<h2 class="text-3xl font-display font-bold text-mahogany mb-6 mt-10">$1</h2>',
		);
		html = html.replace(
			/^# (.*$)/gim,
			'<h1 class="text-4xl font-display font-black text-mahogany mb-8 mt-12">$1</h1>',
		);

		// Bold and italic
		html = html.replace(
			/\*\*(.*?)\*\*/gim,
			'<strong class="text-mahogany font-black">$1</strong>',
		);
		html = html.replace(
			/\*(.*?)\*/gim,
			'<em class="italic text-mahogany/70">$1</em>',
		);

		// Split by double newlines to create paragraphs
		const paragraphs = html.split(/\n\n+/);
		html = paragraphs
			.map((p) => p.trim())
			.filter((p) => p.length > 0)
			.map((p) => {
				// Don't wrap headers in paragraphs
				if (p.startsWith("<h")) {
					return p;
				}
				return `<p class="mb-8 text-ink leading-relaxed text-xl font-serif">${p.replace(/\n/gim, "<br/>")}</p>`;
			})
			.join("");

		return html;
	}
</script>

<svelte:head>
	<title>{post?.title || "Blog Post"} - Mohammed Hamza</title>
</svelte:head>

<div class="bg-parchment min-h-screen">
	{#if post}
		<div class="container mx-auto px-4 py-28 max-w-4xl">
			<button
				on:click={() => goto("/blog")}
				class="group mb-16 flex items-center text-mahogany/60 hover:text-mahogany transition-colors font-display font-bold uppercase tracking-widest text-sm"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-4 w-4 mr-3 group-hover:-translate-x-1 transition-transform"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M10 19l-7-7m0 0l7-7m-7 7h18"
					/>
				</svg>
				Return to Library
			</button>

			<article class="legal-folio p-12 md:p-20 bg-white/50">
				<div class="mb-16 text-center">
					<div
						class="text-brass font-display font-bold mb-6 tracking-[0.3em] uppercase text-xs"
					>
						Dispatch No. {post.id || "001"} — {formatDate(
							post.publishedAt,
						)}
					</div>
					<h1
						class="text-4xl md:text-6xl font-display font-black mb-10 text-mahogany leading-tight uppercase tracking-tighter"
					>
						{post.title}
					</h1>
					<div class="w-24 h-1.5 bg-mahogany mx-auto"></div>
				</div>

				<div class="prose prose-mahogany max-w-none">
					{@html renderMarkdown(post.content)}
				</div>
			</article>
		</div>
	{:else}
		<div class="container mx-auto px-4 py-28 text-center">
			<p
				class="text-mahogany/40 animate-pulse font-display font-bold uppercase tracking-[0.2em]"
			>
				Acquiring Records...
			</p>
		</div>
	{/if}
</div>
