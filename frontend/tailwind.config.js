/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'flyfair-blue': '#0A1E3A', // Deep Blue
        'flyfair-white': '#FFFFFF',
      },
    },
  },
  plugins: [],
}
