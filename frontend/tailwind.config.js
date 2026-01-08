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
				serif: ['PT Serif', 'serif'],
				mono: ['JetBrains Mono', 'monospace']
			}
		}
	},
	plugins: []
};
