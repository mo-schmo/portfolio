/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				cyber: {
					cyan: '#f887ff',
					pink: '#de004e',
					blue: '#321450',
					brown: '#860029',
					dark: '#321450',
					darker: '#29132e',
					'neon-green': '#39FF14',
					'neon-purple': '#BF00FF'
				}
			},
			fontFamily: {
				cyber: ['Orbitron', 'monospace'],
				glitch: ['Rajdhani', 'sans-serif']
			},
			animation: {
				'glow': 'glow 2s ease-in-out infinite alternate',
				'scanline': 'scanline 8s linear infinite',
				'pulse-neon': 'pulse-neon 2s cubic-bezier(0.4, 0, 0.6, 1) infinite'
			},
			keyframes: {
				glow: {
					'0%': { 'text-shadow': '0 0 5px #f887ff, 0 0 10px #f887ff, 0 0 15px #f887ff' },
					'100%': { 'text-shadow': '0 0 10px #f887ff, 0 0 20px #f887ff, 0 0 30px #f887ff' }
				},
				scanline: {
					'0%': { transform: 'translateY(-100%)' },
					'100%': { transform: 'translateY(100vh)' }
				},
				'pulse-neon': {
					'0%, 100%': { opacity: 1, 'box-shadow': '0 0 10px #f887ff, 0 0 20px #f887ff' },
					'50%': { opacity: 0.8, 'box-shadow': '0 0 5px #f887ff, 0 0 10px #f887ff' }
				}
			}
		}
	},
	plugins: []
};
