import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        entryFileNames: "svelte-app-2024-05-14.js",
        assetFileNames: "svelte-app-2024-05-14.[ext]"
      }
    }
  },
  plugins: [svelte()],
})
