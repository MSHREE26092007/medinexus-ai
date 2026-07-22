import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  // GHPAGES=1 builds for https://<user>.github.io/medinexus-ai/
  base: process.env.GHPAGES ? '/medinexus-ai/' : '/',
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      // Avoids CORS entirely in dev: frontend calls /api, Vite forwards to FastAPI
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
