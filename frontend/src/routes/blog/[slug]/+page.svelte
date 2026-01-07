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
			'<h3 class="text-xl font-bold text-cyber-accent mb-2 mt-6">$1</h3>',
		);
		html = html.replace(
			/^## (.*$)/gim,
			'<h2 class="text-2xl font-bold text-cyber-accent mb-3 mt-6">$1</h2>',
		);
		html = html.replace(
			/^# (.*$)/gim,
			'<h1 class="text-3xl font-bold text-cyber-accent mb-4 mt-8">$1</h1>',
		);

		// Bold and italic
		html = html.replace(
			/\*\*(.*?)\*\*/gim,
			'<strong class="text-cyber-cyan">$1</strong>',
		);
		html = html.replace(/\*(.*?)\*/gim, "<em>$1</em>");

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
				return `<p class="mb-4">${p.replace(/\n/gim, "<br/>")}</p>`;
			})
			.join("");

		return html;
	}
</script>

<svelte:head>
	<title>{post?.title || "Blog Post"} - Mohammed Hamza</title>
</svelte:head>

{#if post}
	<div class="container mx-auto px-4 py-12 max-w-4xl">
		<button
			on:click={() => goto("/blog")}
			class="mb-8 text-cyber-text-muted hover:text-cyber-cyan transition-colors"
		>
			← Back to Blog
		</button>

		<article class="glass-card p-8 md:p-12 rounded-lg">
			<h1 class="text-4xl md:text-5xl font-bold mb-4 text-cyber-accent">
				{post.title}
			</h1>
			<div class="text-cyber-text-muted mb-8">
				{formatDate(post.publishedAt)}
			</div>
			<div class="text-lg leading-relaxed">
				{@html renderMarkdown(post.content)}
			</div>
		</article>
	</div>
{:else}
	<div class="container mx-auto px-4 py-12">
		<p class="text-cyber-text-muted">Loading...</p>
	</div>
{/if}
