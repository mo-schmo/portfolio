import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export type ThemeName = 'minimal' | 'neon' | 'matrix' | 'synthwave' | 'terminal';

export interface Theme {
	name: ThemeName;
	label: string;
	icon: string; // SVG path or icon identifier
	colors: {
		cyan: string;
		accent: string;
		text: string;
		'text-muted': string;
		border: string;
		dark: string;
		darker: string;
		card: string;
	};
}

export const themes: Record<ThemeName, Theme> = {
	minimal: {
		name: 'minimal',
		label: 'Minimal',
		icon: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z',
		colors: {
			cyan: '#00d9ff',
			accent: '#58a6ff',
			text: '#e6edf3',
			'text-muted': '#8b949e',
			border: '#30363d',
			dark: '#0d1117',
			darker: '#0a0e1a',
			card: '#161b22'
		}
	},
	neon: {
		name: 'neon',
		label: 'Neon',
		icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
		colors: {
			cyan: '#00ffff',
			accent: '#ff00ff',
			text: '#ffffff',
			'text-muted': '#b0b0b0',
			border: '#00ffff',
			dark: '#000000',
			darker: '#000000',
			card: '#0a0a0a'
		}
	},
	matrix: {
		name: 'matrix',
		label: 'Matrix',
		icon: 'M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5',
		colors: {
			cyan: '#00ff41',
			accent: '#39ff14',
			text: '#00ff41',
			'text-muted': '#00cc33',
			border: '#00ff41',
			dark: '#000000',
			darker: '#000000',
			card: '#0a1a0a'
		}
	},
	synthwave: {
		name: 'synthwave',
		label: 'Synthwave',
		icon: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z',
		colors: {
			cyan: '#f887ff',
			accent: '#de004e',
			text: '#f887ff',
			'text-muted': '#daae6d',
			border: '#f887ff',
			dark: '#29132e',
			darker: '#1a0d1f',
			card: '#321450'
		}
	},
	terminal: {
		name: 'terminal',
		label: 'Terminal',
		icon: 'M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-4h16v4zm0-6H4V6h16v6z',
		colors: {
			cyan: '#00ff88',
			accent: '#88ff00',
			text: '#00ff88',
			'text-muted': '#66cc66',
			border: '#00ff88',
			dark: '#0a0a0a',
			darker: '#000000',
			card: '#1a1a1a'
		}
	}
};

function getInitialTheme(): ThemeName {
	if (!browser) return 'minimal';
	const stored = localStorage.getItem('theme') as ThemeName;
	return stored && themes[stored] ? stored : 'minimal';
}

export const currentTheme = writable<ThemeName>(getInitialTheme());

if (browser) {
	// Apply initial theme immediately
	const initialTheme = getInitialTheme();
	applyTheme(themes[initialTheme]);
	
	// Subscribe to theme changes
	currentTheme.subscribe((theme) => {
		localStorage.setItem('theme', theme);
		applyTheme(themes[theme]);
	});
}

export function applyTheme(theme: Theme) {
	if (!browser) return;
	
	const root = document.documentElement;
	Object.entries(theme.colors).forEach(([key, value]) => {
		root.style.setProperty(`--cyber-${key}`, value);
	});
	
	// Update body background gradient colors dynamically
	const cyanRgb = hexToRgb(theme.colors.cyan);
	const accentRgb = hexToRgb(theme.colors.accent);
	
	if (cyanRgb && accentRgb) {
		const cyanMix = `rgba(${cyanRgb.r}, ${cyanRgb.g}, ${cyanRgb.b}, 0.03)`;
		const accentMix = `rgba(${accentRgb.r}, ${accentRgb.g}, ${accentRgb.b}, 0.02)`;
		root.style.setProperty('--gradient-cyan', cyanMix);
		root.style.setProperty('--gradient-accent', accentMix);
	}
}

function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
	const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
	return result
		? {
				r: parseInt(result[1], 16),
				g: parseInt(result[2], 16),
				b: parseInt(result[3], 16)
			}
		: null;
}

export function setTheme(themeName: ThemeName) {
	currentTheme.set(themeName);
}
