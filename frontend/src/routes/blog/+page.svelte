<script lang="ts">
	import { mockBlogPosts } from '$lib/stores/mockData';
	
	function formatDate(dateString: string): string {
		const date = new Date(dateString);
		return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
	}
</script>

<svelte:head>
	<title>Blog - Mohammed Hamza</title>
</svelte:head>

<div class="container mx-auto px-4 py-12">
	<h1 class="text-5xl font-bold mb-12 neon-text text-center">Blog</h1>
	
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
		{#each mockBlogPosts as post}
			<a
				href="/blog/{post.slug}"
				class="glass-card p-6 rounded-lg cursor-pointer glow-on-hover h-full flex flex-col block"
			>
				<h2 class="text-2xl font-bold text-cyber-pink mb-4 neon-text">
					{post.title}
				</h2>
				<p class="text-cyber-cyan/80 mb-4 flex-grow">
					{post.excerpt}
				</p>
				<div class="text-cyber-cyan/60 text-sm">
					{formatDate(post.publishedAt)}
				</div>
			</a>
		{/each}
	</div>
</div>
