import type {
  AnalysisResult,
  DetectHealth,
  DetectResult,
  PrivateResult,
  PrivateRestore,
  SelfTest,
} from "./types";

// Existing setting, unchanged: NEXT_PUBLIC_API_URL, or the /api/backend proxy path.
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/backend";
// The trained domain detector lives at /api/v1/detect on the same server.
const ORIGIN = API_BASE.replace(/\/api\/backend\/?$/, "");

export class ApiError extends Error {}

function messageFromDetail(detail: unknown): string | null {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    const parts = detail
      .map((d) => (d && typeof d === "object" && "msg" in d ? String((d as { msg: unknown }).msg) : null))
      .filter((m): m is string => Boolean(m));
    return parts.length ? parts.join(". ") : null;
  }
  return null;
}

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(url, init);
  } catch {
    throw new ApiError(
      "Can't reach the analysis server. Start the backend (uvicorn app.main:app) and try again."
    );
  }

  let data: unknown = null;
  try {
    data = await response.json();
  } catch {
    // body was not JSON; handled below
  }

  if (!response.ok) {
    const detail =
      data && typeof data === "object" && "detail" in data
        ? messageFromDetail((data as { detail: unknown }).detail)
        : null;
    throw new ApiError(detail ?? `The server returned an error (${response.status}).`);
  }
  return data as T;
}

export function detectDomain(url: string): Promise<DetectResult> {
  return request<DetectResult>(`${ORIGIN}/api/v1/detect`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
}

export function fetchModelHealth(): Promise<DetectHealth> {
  return request<DetectHealth>(`${ORIGIN}/api/v1/detect/health`);
}

export function analyzeText(text: string): Promise<AnalysisResult> {
  return request<AnalysisResult>(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
}

export function analyzeFile(kind: "image" | "email", file: File): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append("file", file);
  return request<AnalysisResult>(`${API_BASE}/analyze-${kind}`, {
    method: "POST",
    body: formData,
  });
}

export function analyzePrivately(text: string, protectedTerms: string[]): Promise<PrivateResult> {
  return request<PrivateResult>(`${ORIGIN}/api/v1/private/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, protected_terms: protectedTerms }),
  });
}

export function restorePrivate(requestId: string, shares: string[]): Promise<PrivateRestore> {
  return request<PrivateRestore>(`${ORIGIN}/api/v1/private/restore`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ request_id: requestId, shares }),
  });
}

export function runSelfTest(): Promise<SelfTest> {
  return request<SelfTest>(`${ORIGIN}/api/v1/private/selftest`);
}
