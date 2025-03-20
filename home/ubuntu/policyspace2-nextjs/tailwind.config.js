/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'blue': {
          100: '#dbeafe',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        'gray': {
          100: '#f3f4f6',
          300: '#d1d5db',
          600: '#4b5563',
          800: '#1f2937',
        },
      },
    },
  },
  plugins: [],
}
