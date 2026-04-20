const rawBackendUrl = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export const backendUrl = rawBackendUrl.replace(/\/+$/, "");