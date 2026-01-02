<script lang="ts">
	const socialLinks = [
		{ name: 'GitHub', url: 'https://github.com/mo-schmo' },
		{ name: 'LinkedIn', url: 'https://www.linkedin.com/in/mohammed-h-a7a275118/' },
		{ name: 'Email', url: 'mailto:HAMZA.ABJOL.MOHAMMED@GMAIL.COM' }
	];
</script>

<footer class="border-t-2 border-t-cyber-cyan-30 mt-20 py-8">
	<div class="container mx-auto px-4">
		<div class="flex flex-col md:flex-row justify-between items-center">
			<p class="text-cyber-text-muted mb-4 md:mb-0">
				© 2025 Mohammed Hamza. All rights reserved.
			</p>
			<div class="flex space-x-6">
				{#each socialLinks as link}
					<a
						href={link.url}
						target="_blank"
						rel="noopener noreferrer"
						class="text-cyber-text-muted hover:text-cyber-cyan transition-colors"
					>
						{link.name}
					</a>
				{/each}
			</div>
		</div>
	</div>
</footer>
