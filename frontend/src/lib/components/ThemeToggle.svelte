<script lang="ts">
	import { currentTheme, themes, type ThemeName } from '$lib/stores/theme';
	
	const themeOrder: ThemeName[] = ['minimal', 'neon', 'matrix', 'synthwave', 'terminal'];
	
	function cycleTheme() {
		const current = $currentTheme;
		const currentIndex = themeOrder.indexOf(current);
		const nextIndex = (currentIndex + 1) % themeOrder.length;
		currentTheme.set(themeOrder[nextIndex]);
	}
	
	$: currentThemeData = themes[$currentTheme];
</script>

<button
	on:click={cycleTheme}
	class="p-2 border border-cyber-border hover:border-cyber-cyan transition-all rounded-lg text-cyber-text-muted hover:text-cyber-cyan hover:bg-cyber-cyan-10"
	aria-label="Cycle theme (Current: {currentThemeData.label})"
	title="Cycle theme: {currentThemeData.label}"
>
	<svg 
		width="20" 
		height="20" 
		viewBox="0 0 24 24" 
		fill="none" 
		xmlns="http://www.w3.org/2000/svg"
		class="theme-icon"
	>
		<path 
			d={currentThemeData.icon}
			fill="currentColor"
		/>
	</svg>
</button>

<style>
	.theme-icon {
		transition: transform 0.3s ease;
	}
	
	button:hover .theme-icon {
		transform: rotate(90deg);
	}
</style>
