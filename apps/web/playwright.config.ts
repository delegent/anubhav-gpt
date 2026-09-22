import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  use: {
    baseURL: "http://localhost:5173",
    ...devices["Desktop Chrome"],
  },
  webServer: [{ command: "vite --host 127.0.0.1", port: 5173, reuseExistingServer: true }],
});
