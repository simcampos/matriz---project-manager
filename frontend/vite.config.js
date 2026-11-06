import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const apiProxyTarget = process.env.VITE_API_PROXY_TARGET;

export default defineConfig({
  envDir: "..",
  plugins: [react()],
  server: {
    allowedHosts: apiProxyTarget ? ["e2e-frontend"] : undefined,
    port: 5173,
    strictPort: true,
    proxy: apiProxyTarget
      ? {
          "/api": {
            target: apiProxyTarget,
            changeOrigin: true,
          },
        }
      : undefined,
  },
});
