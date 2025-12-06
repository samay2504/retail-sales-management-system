/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00E5CF',
          50: '#B8FFF8',
          100: '#A3FFF6',
          200: '#7AFFF1',
          300: '#52FFED',
          400: '#29FFE9',
          500: '#00E5CF',
          600: '#00ADA0',
          700: '#007571',
          800: '#003D42',
          900: '#000513',
        },
        purple: {
          DEFAULT: '#7C3AED',
          50: '#E8DFFB',
          100: '#DACCF9',
          200: '#BEA6F5',
          300: '#A280F0',
          400: '#865AEC',
          500: '#7C3AED',
          600: '#6522D6',
          700: '#4F1AA7',
          800: '#391278',
          900: '#230A49',
        },
        cyan: {
          DEFAULT: '#06B6D4',
          50: '#B8F6FF',
          100: '#9EF3FF',
          200: '#6BEDFF',
          300: '#38E7FF',
          400: '#06D8F7',
          500: '#06B6D4',
          600: '#0595B0',
          700: '#03748B',
          800: '#025366',
          900: '#013241',
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-cta': 'linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%)',
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'glow-cyan': '0 0 20px rgba(6, 182, 212, 0.5)',
        'glow-purple': '0 0 20px rgba(124, 58, 237, 0.5)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
