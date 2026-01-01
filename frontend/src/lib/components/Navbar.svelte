<script lang="ts">
	import { page } from '$app/stores';
	
	const navItems = [
		{ href: '/', label: 'Home' },
		{ href: '/projects', label: 'Projects' },
		{ href: '/blog', label: 'Blog' },
		{ href: '/contact', label: 'Contact' }
	];
</script>

<nav class="fixed top-0 w-full z-50 glass-card border-b-2 border-cyber-cyan/50">
	<div class="container mx-auto px-4 py-4">
		<div class="flex items-center justify-between">
			<a href="/" class="text-2xl font-bold neon-text glow-on-hover">
				MH
			</a>
			<ul class="flex space-x-8">
				{#each navItems as item}
					<li>
						<a
							href={item.href}
							class="glow-on-hover transition-colors duration-300 {$page.url.pathname === item.href ? 'text-cyber-cyan neon-text' : 'text-cyber-cyan/70 hover:text-cyber-cyan'}"
						>
							{item.label}
						</a>
					</li>
				{/each}
			</ul>
		</div>
	</div>
</nav>
