/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/app/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        'black': '#282828',
        'red': '#cc241d',
        'green': '#98971a',
        'yellow': '#d79921',
        'blue': '#458588',
        'purple': '#b16286',
        'aqua': '#689d6a',
        'orange': '#d65d0e',
        'white': '#ebdbb2',
        'gray': '#928374'
    }
  },
  plugins: [],
}}
