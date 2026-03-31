/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        pln: {
          blue: '#1e88e5', // Example blue
          yellow: '#fdd835', // Example yellow
          red: '#e53935',
        }
      }
    },
  },
  plugins: [],
}
