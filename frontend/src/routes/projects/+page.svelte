<script lang="ts">
	export let data;
	$: projects = data.projects || [];

	let filter = "all";
	const filters = ["all", "featured"];

	function parseTechnologies(techStr: string): string[] {
		try {
			const parsed = JSON.parse(techStr);
			if (typeof parsed === "string") {
				return JSON.parse(parsed);
			}
			return parsed;
		} catch (e) {
			return [];
		}
	}

	$: filteredProjects =
		filter === "featured" ? projects.filter((p) => p.featured) : projects;
</script>

<svelte:head>
	<title>Projects - Mohammed Hamza</title>
</svelte:head>

<div class="container mx-auto px-4 py-28 max-w-6xl">
	<div class="text-center mb-24">
		<h1
			class="text-6xl md:text-8xl font-display font-black mb-6 text-mahogany tracking-tighter"
		>
			Folio of Works
		</h1>
		<div class="w-24 h-1 bg-mahogany mx-auto mb-8"></div>
		<p class="text-xl text-mahogany/70 max-w-2xl mx-auto font-serif italic">
			A curated record of architectural implementations and digital
			solutions.
		</p>
	</div>

	<!-- Filter Buttons -->
	<div class="flex justify-center gap-6 mb-20">
		{#each filters as f}
			<button
				class="px-8 py-2 font-display font-bold uppercase tracking-widest text-xs transition-all {filter ===
				f
					? 'bg-mahogany text-parchment border-2 border-mahogany shadow-[4px_4px_0px_rgba(148,122,70,0.4)]'
					: 'bg-transparent text-mahogany/60 hover:text-mahogany border-2 border-transparent'}"
				on:click={() => (filter = f)}
			>
				{f === "all" ? "All Records" : "Featured Exhibits"}
			</button>
		{/each}
	</div>

	<!-- Projects Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
		{#each filteredProjects as project}
			<a
				href="/projects/{project.slug}"
				class="legal-folio flex flex-col group overflow-hidden bg-white/50 cursor-pointer"
			>
				<div
					class="relative overflow-hidden aspect-video border-b border-paper-line/50"
				>
					{#if project.imageUrl}
						<img
							src={project.imageUrl}
							alt={project.title}
							class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 grayscale hover:grayscale-0 opacity-80 hover:opacity-100"
						/>
					{:else}
						<div
							class="w-full h-full bg-parchment-dark/50 flex items-center justify-center"
						>
							<span class="text-4xl opacity-20">⚡</span>
						</div>
					{/if}
				</div>

				<div class="p-10 flex flex-col flex-grow">
					<h2
						class="text-2xl font-display font-black text-mahogany mb-4 uppercase tracking-tight"
					>
						{project.title}
					</h2>

					<p
						class="mb-8 flex-grow text-ink/80 font-serif leading-relaxed italic"
					>
						{project.description}
					</p>

					<div class="mb-10">
						<div class="flex flex-wrap gap-2">
							{#each parseTechnologies(project.technologies) as tech}
								<span
									class="px-3 py-1 bg-mahogany/5 border border-mahogany/10 rounded-sm text-[10px] font-display font-bold uppercase tracking-widest text-mahogany/70"
								>
									{tech}
								</span>
							{/each}
						</div>
					</div>

					<div class="flex gap-4">
						<div
							class="flex-1 text-center py-3 font-display font-bold uppercase tracking-widest text-xs bg-mahogany text-parchment border border-mahogany group-hover:bg-mahogany-light transition-all shadow-[2px_2px_0px_rgba(0,0,0,0.1)]"
						>
							Examine Record
						</div>
					</div>
				</div>
			</a>
		{/each}
	</div>
</div>
