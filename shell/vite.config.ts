import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import wyw from "@wyw-in-js/vite";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/static/",
  build: {
    manifest: true,
    rollupOptions: {
      input: "/src/main.tsx",
    },
    outDir: "../wagtail_reactadmin/static",
  },
  plugins: [
    react(),
    wyw({
      babelOptions: {
        presets: ["@babel/preset-typescript"],
      },
    }),
  ],
  server: {
    host: "0.0.0.0",
    cors: {
      origin: "http://192.168.122.58:9000",
    },
  },
});
