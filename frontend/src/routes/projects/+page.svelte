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
	<h1 class="text-5xl font-bold mb-8 text-cyber-text text-center">Projects</h1>
	
	<!-- Filter Buttons -->
	<div class="flex justify-center gap-4 mb-12">
		{#each filters as f}
			<button
				class="px-6 py-2 neon-border transition-all {filter === f ? 'bg-cyber-cyan-20 text-cyber-cyan' : 'text-cyber-text-muted hover:text-cyber-cyan'}"
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
						class="w-full h-48 object-cover rounded-lg mb-4 border border-cyber-cyan-30"
					/>
				{:else}
					<div class="w-full h-48 bg-cyber-cyan-10 rounded-lg mb-4 border border-cyber-cyan-30 flex items-center justify-center">
						<span class="text-cyber-cyan-50 text-4xl">⚡</span>
					</div>
				{/if}
				
				<h2 class="text-2xl font-bold text-cyber-accent mb-3">
					{project.title}
				</h2>
				
				<p class="mb-4 flex-grow">
					{project.description}
				</p>
				
				<div class="mb-4">
					<div class="flex flex-wrap gap-2">
						{#each project.technologies as tech}
							<span class="px-3 py-1 bg-cyber-cyan-10 border border-cyber-border rounded text-sm text-cyber-text-muted">
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
							class="px-4 py-2 border border-cyber-border hover:border-cyber-cyan text-cyber-text-muted hover:text-cyber-cyan transition-colors text-sm"
						>
							GitHub
						</a>
					{/if}
					{#if project.liveUrl}
						<a
							href={project.liveUrl}
							target="_blank"
							rel="noopener noreferrer"
							class="px-4 py-2 border border-cyber-border hover:border-cyber-accent text-cyber-text-muted hover:text-cyber-accent transition-colors text-sm"
						>
							Live Demo
						</a>
					{/if}
				</div>
			</div>
		{/each}
	</div>
</div>
