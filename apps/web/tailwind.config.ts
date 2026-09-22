import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        graphite: "#101116",
        panel: "#171922",
        line: "#2a2e3b",
        accent: "#7c8cff",
      },
    },
  },
  plugins: [typography],
} satisfies Config;
