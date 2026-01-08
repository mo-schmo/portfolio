<script lang="ts">
	const socialLinks = [
		{ name: "GitHub", url: "https://github.com/mo-schmo" },
		{
			name: "LinkedIn",
			url: "https://www.linkedin.com/in/mohammed-h-a7a275118/",
		},
		{ name: "Email", url: "mailto:HAMZA.ABJOL.MOHAMMED@GMAIL.COM" },
	];
</script>

<footer class="border-t border-paper-line mt-32 py-16 bg-parchment-dark/30">
	<div class="container mx-auto px-4 max-w-6xl">
		<div
			class="flex flex-col md:flex-row justify-between items-center gap-10"
		>
			<div class="text-center md:text-left">
				<a
					href="/"
					class="text-2xl font-display font-bold text-mahogany tracking-tighter block mb-2"
					>HAMZA & CO.</a
				>
				<p class="text-mahogany/60 text-sm font-serif italic">
					Est. 2021 — Dedicated to scalable excellence.
				</p>
			</div>
			<div class="flex space-x-10">
				{#each socialLinks as link}
					<a
						href={link.url}
						target="_blank"
						rel="noopener noreferrer"
						class="text-mahogany/70 hover:text-mahogany transition-colors font-display font-bold uppercase tracking-widest text-xs border-b border-transparent hover:border-mahogany"
					>
						{link.name}
					</a>
				{/each}
			</div>
		</div>
		<div class="mt-12 pt-8 border-t border-paper-line/50 text-center">
			<p
				class="text-mahogany/40 text-xs uppercase tracking-widest font-display"
			>
				© 2026 Mohammed Hamza • All Rights Reserved
			</p>
		</div>
	</div>
</footer>
