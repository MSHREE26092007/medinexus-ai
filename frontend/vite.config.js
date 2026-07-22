import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      // Avoids CORS entirely in dev: frontend calls /api, Vite forwards to FastAPI
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
