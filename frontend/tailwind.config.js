/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#0B0F17',
          sidebar: '#0D1420',
          card: '#111827',
          elevated: '#172033',
        },
        border: {
          subtle: '#253247',
          active: '#00D6C9',
        },
        accent: {
          cyan: '#00D6C9',
          emerald: '#10B981',
          amber: '#F59E0B',
          rose: '#EF4444',
        },
        text: {
          primary: '#F8FAFC',
          secondary: '#94A3B8',
          muted: '#64748B',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'card': '0 4px 16px -2px rgba(0, 0, 0, 0.4)',
        'cyan-glow': '0 0 16px -2px rgba(0, 214, 201, 0.3)',
        'amber-glow': '0 0 16px -2px rgba(245, 158, 11, 0.4)',
      },
    },
  },
  plugins: [],
}

