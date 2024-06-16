import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/

export default defineConfig(({ command, mode }) => {
  // Load env file based on `mode` in the current working directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), "");
  return {
    // vite config
    plugins: [vue()],
    define: {
      __APP_ENV__: JSON.stringify(env.APP_ENV)
    },
    root: "./client/user_module",
    server: {
      proxy: {
        "/api": "http://localhost:4022"
      }
    }
  };
});
