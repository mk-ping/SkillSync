/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0A0A0C",
        panel: "rgba(255,255,255,0.035)",
        border: "rgba(255,255,255,0.08)",
        mint: "#5EEAD4",
        mintDeep: "#2DD4BF",
        violet: "#A78BFA",
        rose: "#FB7185",
        textPrimary: "#F4F4F5",
        textMuted: "#8A8A93",
      },
      fontFamily: {
        heading: ["Familjen Grotesk", "sans-serif"],
        body: ["Public Sans", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
      backdropBlur: {
        glass: "16px",
      },
      borderRadius: {
        card: "14px",
      },
    },
  },
  plugins: [],
}
