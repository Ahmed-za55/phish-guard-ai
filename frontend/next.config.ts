import type { NextConfig } from "next";

// In development the browser talks only to Next.js, and Next.js forwards API calls to the
// FastAPI backend. That avoids any CORS setup. Set BACKEND_URL to forward somewhere else
// (for example a deployed backend). In production without BACKEND_URL nothing is rewritten.
const backend =
  process.env.BACKEND_URL ??
  (process.env.NODE_ENV === "development" ? "http://127.0.0.1:8000" : undefined);

const nextConfig: NextConfig = {
  async rewrites() {
    if (!backend) return [];
    return [
      { source: "/api/backend/:path*", destination: `${backend}/api/backend/:path*` },
      { source: "/api/v1/:path*", destination: `${backend}/api/v1/:path*` },
    ];
  },
};

export default nextConfig;
