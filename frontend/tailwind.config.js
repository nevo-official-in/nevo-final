/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'playfair': ['Playfair Display', 'serif'],
      },
      colors: {
        'nevo-black': '#0a0a0a',
        'nevo-gray': '#1a1a1a',
        'nevo-red': '#c41e3a',
      },
    },
  },
  plugins: [],
}