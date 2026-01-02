<script lang="ts">
	import { page } from '$app/stores';
	import ThemeToggle from './ThemeToggle.svelte';
	
	const navItems = [
		{ href: '/', label: 'Home' },
		{ href: '/projects', label: 'Projects' },
		{ href: '/blog', label: 'Blog' },
		{ href: '/contact', label: 'Contact' }
	];
</script>

<nav class="fixed top-0 w-full z-50 bg-cyber-card-95 backdrop-blur-md border-b border-cyber-border">
	<div class="container mx-auto px-4 py-4">
		<div class="flex items-center justify-between">
			<a href="/" class="text-2xl font-bold text-cyber-text hover:text-cyber-cyan transition-colors duration-300">
				MH
			</a>
			<div class="flex items-center space-x-8">
				<ul class="flex space-x-8">
					{#each navItems as item}
						<li>
							<a
								href={item.href}
								class="transition-colors duration-300 {$page.url.pathname === item.href ? 'text-cyber-cyan' : 'text-cyber-text-muted hover:text-cyber-cyan'}"
							>
								{item.label}
							</a>
						</li>
					{/each}
				</ul>
				<ThemeToggle />
			</div>
		</div>
	</div>
</nav>
