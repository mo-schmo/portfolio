/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				mahogany: {
					DEFAULT: '#2d1b1b',
					light: '#4a2c2c',
					dark: '#1a1010'
				},
				parchment: {
					DEFAULT: '#fbf9f1',
					dark: '#f0ede0',
					aged: '#e8e2c8'
				},
				brass: {
					DEFAULT: '#947a46',
					light: '#b59e6d',
					dark: '#735f37'
				},
				ink: '#1a1a1a',
				'paper-line': '#d1c7b1'
			},
			fontFamily: {
				display: ['Playfair Display', 'serif'],
				// Body serif: Newsreader (contemporary, screen-optimized) with PT Serif fallback.
				serif: ['Newsreader', 'PT Serif', 'serif'],
				ptserif: ['PT Serif', 'serif'],
				mono: ['JetBrains Mono', 'monospace']
			},
			fontSize: {
				'step--1': 'var(--step--1)',
				'step-0': 'var(--step-0)',
				'step-1': 'var(--step-1)',
				'step-2': 'var(--step-2)',
				'step-3': 'var(--step-3)',
				'step-4': 'var(--step-4)',
				'step-5': 'var(--step-5)',
				'step-6': 'var(--step-6)',
				'step-7': 'var(--step-7)'
			}
		}
	},
	plugins: []
};
