import { shouldDispatchSessionExpiredEvent } from "./sessionExpired";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "");

export const sessionExpiredEvent = "matriz:session-expired";

export function getCsrfCookie() {
  const cookie = document.cookie
    .split("; ")
    .find((entry) => entry.startsWith("csrftoken="));
  return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
}

export async function apiRequest(path, options = {}) {
  if (!apiBaseUrl) {
    throw new Error("Configuração VITE_API_BASE_URL em falta.");
  }

  const response = await fetch(`${apiBaseUrl}${path}`, {
    credentials: "include",
    ...options,
  });
  if (shouldDispatchSessionExpiredEvent(path, response.status)) {
    window.dispatchEvent(new Event(sessionExpiredEvent));
  }
  return response;
}

export async function ensureCsrfCookie() {
  const response = await apiRequest("/csrf/");
  if (!response.ok || !getCsrfCookie()) {
    throw new Error("Não foi possível preparar a proteção CSRF.");
  }
}

export async function getResponseError(response, fallback) {
  if (!response.headers.get("content-type")?.includes("application/json")) {
    return fallback;
  }
  const body = await response.json();
  if (typeof body.detail === "string") {
    return body.detail;
  }
  const firstError = Object.values(body)
    .flat()
    .find((value) => typeof value === "string");
  return firstError || fallback;
}

export function getRequestError(error, fallback) {
  if (error instanceof TypeError) {
    return "Não foi possível comunicar com o servidor. Verifica a ligação e tenta novamente.";
  }
  return error?.message || fallback;
}
