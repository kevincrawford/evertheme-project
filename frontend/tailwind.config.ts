import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f0f4ff",
          100: "#dde8ff",
          200: "#c3d4ff",
          300: "#9db6ff",
          400: "#748eff",
          500: "#5469ff",
          600: "#3d47f5",
          700: "#3337e0",
          800: "#2a2db5",
          900: "#282d8e",
          950: "#191a55",
        },
      },
    },
  },
  plugins: [],
};

export default config;
