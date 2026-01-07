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

<div class="container mx-auto px-4 py-12">
	<h1 class="text-5xl font-bold mb-12 text-cyber-text text-center">Blog</h1>

	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
		{#each posts as post}
			<a
				href="/blog/{post.slug}"
				class="glass-card p-6 rounded-lg cursor-pointer glow-on-hover h-full flex flex-col block"
			>
				<h2 class="text-2xl font-bold text-cyber-accent mb-4">
					{post.title}
				</h2>
				<p class="mb-4 flex-grow text-cyber-text-muted">
					{post.excerpt}
				</p>
				<div class="text-cyber-text-muted text-sm">
					{formatDate(post.publishedAt)}
				</div>
			</a>
		{/each}
	</div>
</div>
