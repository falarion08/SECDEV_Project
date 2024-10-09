/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js"
],
  theme: {
    extend: {
      screens: {
        xs: "375px",
      },
      colors: {
        "theme": "#0284C7",
        "btn-dflt":"#3B82F6",
        "workspace-item-bg": "#F0F9FF",
      },
      fontFamily: {
        "fredoka": ["Fredoka", "sans-serif"],
        "inter": ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
}

