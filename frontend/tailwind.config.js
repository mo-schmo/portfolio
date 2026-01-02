/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				cyber: {
					cyan: 'var(--cyber-cyan)',
					accent: 'var(--cyber-accent)',
					text: 'var(--cyber-text)',
					'text-muted': 'var(--cyber-text-muted)',
					border: 'var(--cyber-border)',
					dark: 'var(--cyber-dark)',
					darker: 'var(--cyber-darker)',
					card: 'var(--cyber-card)'
				}
			},
			fontFamily: {
				cyber: ['Inter', 'system-ui', 'sans-serif'],
				mono: ['JetBrains Mono', 'monospace']
			},
			animation: {
				'glow': 'glow 2s ease-in-out infinite alternate'
			},
			keyframes: {
				glow: {
					'0%': { opacity: 0.8 },
					'100%': { opacity: 1 }
				},
				scanline: {
					'0%': { transform: 'translateY(-100%)' },
					'100%': { transform: 'translateY(100vh)' }
				}
			}
		}
	},
	plugins: []
};
