import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // or your preferred dev port
    proxy: {
      '/start-detection': 'http://localhost:8000',
      '/stop-detection': 'http://localhost:8000',
      '/toggle-sound': 'http://localhost:8000',
      '/detections': 'http://localhost:8000',
    },
  },
});
