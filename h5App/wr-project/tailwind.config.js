/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#165DFF',
        secondary: '#FF7D00',
        neutral: {
          100: '#F5F7FA',
          200: '#E4E7ED',
          300: '#C0C4CC',
          400: '#909399',
          500: '#606266',
          600: '#303133',
        }
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
    }
  },
  plugins: [],
}