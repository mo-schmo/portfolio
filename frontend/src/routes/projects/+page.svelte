<script lang="ts">
	import { mockProjects } from '$lib/stores/mockData';
	
	let filter = 'all';
	const filters = ['all', 'featured'];
	
	$: filteredProjects = filter === 'featured' 
		? mockProjects.filter(p => p.featured)
		: mockProjects;
</script>

<svelte:head>
	<title>Projects - Mohammed Hamza</title>
</svelte:head>

<div class="container mx-auto px-4 py-12">
	<h1 class="text-5xl font-bold mb-8 neon-text text-center">Projects</h1>
	
	<!-- Filter Buttons -->
	<div class="flex justify-center gap-4 mb-12">
		{#each filters as f}
			<button
				class="px-6 py-2 neon-border glow-on-hover bg-black/20 transition-all {filter === f ? 'bg-cyber-cyan/20 text-cyber-cyan' : 'text-cyber-cyan/70'}"
				on:click={() => filter = f}
			>
				{f.charAt(0).toUpperCase() + f.slice(1)}
			</button>
		{/each}
	</div>
	
	<!-- Projects Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
		{#each filteredProjects as project}
			<div class="glass-card p-6 rounded-lg h-full flex flex-col">
				{#if project.imageUrl}
					<img
						src={project.imageUrl}
						alt={project.title}
						class="w-full h-48 object-cover rounded-lg mb-4 border border-cyber-cyan/30"
					/>
				{:else}
					<div class="w-full h-48 bg-cyber-cyan/10 rounded-lg mb-4 border border-cyber-cyan/30 flex items-center justify-center">
						<span class="text-cyber-cyan/50 text-4xl">⚡</span>
					</div>
				{/if}
				
				<h2 class="text-2xl font-bold text-cyber-pink mb-3 neon-text">
					{project.title}
				</h2>
				
				<p class="mb-4 flex-grow">
					{project.description}
				</p>
				
				<div class="mb-4">
					<div class="flex flex-wrap gap-2">
						{#each project.technologies as tech}
							<span class="px-3 py-1 bg-cyber-cyan/10 border border-cyber-cyan/30 rounded text-sm text-cyber-cyan">
								{tech}
							</span>
						{/each}
					</div>
				</div>
				
				<div class="flex gap-4 mt-auto">
					{#if project.githubUrl}
						<a
							href={project.githubUrl}
							target="_blank"
							rel="noopener noreferrer"
							class="px-4 py-2 border border-cyber-cyan/50 hover:border-cyber-cyan glow-on-hover text-sm"
						>
							GitHub
						</a>
					{/if}
					{#if project.liveUrl}
						<a
							href={project.liveUrl}
							target="_blank"
							rel="noopener noreferrer"
							class="px-4 py-2 border border-cyber-pink/50 hover:border-cyber-pink glow-on-hover text-sm"
						>
							Live Demo
						</a>
					{/if}
				</div>
			</div>
		{/each}
	</div>
</div>
