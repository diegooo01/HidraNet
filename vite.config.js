import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/generate_map': {
        target: 'http://127.0.0.1:5000', // Dirección de tu servidor Flask
        changeOrigin: true,
        secure: false
      }
    }
  },
  base: './',

});
