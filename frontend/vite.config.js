import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    // ❌ tailwindcss() plugin REMOVE kar - Tailwind v3 ke liye zaroori nahi
  ],
})