/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        cyber: {
          background: '#0F172A',
          panel: '#111827',
          elevated: '#1E293B',
          border: '#334155',
          cyan: '#38BDF8',
          green: '#22C55E',
          amber: '#F59E0B',
          red: '#EF4444',
          text: '#F8FAFC',
          muted: '#94A3B8',
        },
      },
      boxShadow: {
        glow: '0 0 32px rgba(56, 189, 248, 0.16)',
      },
    },
  },
  plugins: [],
};
