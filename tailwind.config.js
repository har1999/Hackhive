/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        worker: {
          primary: '#0f766e',
          accent: '#f59e0b',
          urgent: '#dc2626',
          info: '#2563eb',
          success: '#16a34a',
        },
        contractor: {
          primary: '#1d4ed8',
          accent: '#ea580c',
          danger: '#b91c1c',
        },
      },
      boxShadow: {
        panel: '0 10px 30px rgba(2, 44, 34, 0.12)',
      },
    },
  },
  plugins: [],
}
