import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.E2E_BASE_URL || "http://127.0.0.1:5174";
const apiBaseURL = process.env.E2E_API_BASE_URL || "http://127.0.0.1:8001/api";
const frontendOrigin = new URL(baseURL).origin;
const e2ePassword = process.env.DEMO_PM_PASSWORD;
const chromiumExecutablePath =
  process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const dockerWebServers = process.env.E2E_DOCKER === "true";

if (!e2ePassword) {
  throw new Error(
    "DEMO_PM_PASSWORD must be set in the repository .env file for E2E tests.",
  );
}

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [["list"], ["html", { outputFolder: "playwright-report", open: "never" }]],
  use: {
    ...devices["Desktop Chrome"],
    baseURL,
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        ...(chromiumExecutablePath
          ? { launchOptions: { executablePath: chromiumExecutablePath } }
          : {}),
      },
    },
  ],
  webServer: dockerWebServers
    ? []
    : [
    {
      command: ".venv/bin/python backend/manage.py runserver 127.0.0.1:8001 --noreload",
      cwd: "..",
      url: `${apiBaseURL}/health/`,
      reuseExistingServer: false,
      timeout: 30_000,
      env: {
        POSTGRES_DB: "matriz_e2e",
        POSTGRES_PORT: "5433",
        DJANGO_DEBUG: "true",
        DJANGO_CORS_ALLOWED_ORIGINS: frontendOrigin,
        DJANGO_CSRF_TRUSTED_ORIGINS: frontendOrigin,
      },
    },
    {
      command: "npm run dev -- --host 127.0.0.1 --port 5174",
      url: baseURL,
      reuseExistingServer: false,
      timeout: 30_000,
      env: {
        VITE_API_BASE_URL: apiBaseURL,
      },
    },
  ],
});

export const e2eCredentials = {
  email: process.env.E2E_PM_EMAIL || "pm@matriz.dev",
  password: e2ePassword,
};

export const e2eApiBaseURL = apiBaseURL;
