"use client";

import { DragEvent, useRef, useState } from "react";

type URLAnalysis = {
  url: string;
  hostname: string;
  risk_score: number;
  risk_level: string;
  reasons: string[];
};

type AttachmentAnalysis = {
  filename: string;
  risk_score: number;
  risk_level: string;
  reasons: string[];
};

type EmailDetails = {
  sender_name: string;
  sender_email: string;
  sender_domain: string;
  reply_email: string;
  reply_to_domain: string;
  subject: string;
  attachments: string[];
  attachment_analysis: AttachmentAnalysis[];
  security_flags: string[];
};

type RiskContribution = {
  signal: string;
  source: string;
  points: number;
};

type RiskBreakdown = {
  raw_score: number;
  risk_score: number;
  risk_level: string;
  capped: boolean;
  highest_url_score: number;
  contributions: RiskContribution[];
};

type AnalysisResult = {
  is_phishing: boolean;
  confidence: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  risk_score: number;
  threats: string[];
  evidence: string[];
  recommendations: string[];
  urls: URLAnalysis[];
  email_details: EmailDetails | null;
  risk_breakdown: RiskBreakdown | null;
};

type Mode = "text" | "image" | "email";

const riskStyles: Record<string, string> = {
  LOW: "border-emerald-500/30 bg-emerald-500/10 text-emerald-400",
  MEDIUM: "border-yellow-500/30 bg-yellow-500/10 text-yellow-400",
  HIGH: "border-orange-500/30 bg-orange-500/10 text-orange-400",
  CRITICAL: "border-red-500/30 bg-red-500/10 text-red-400",
};

export default function Home() {
  const [mode, setMode] = useState<Mode>("text");
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fileInputRef = useRef<HTMLInputElement>(null);

  function clearAll() {
    setText("");
    setFile(null);
    setPreview(null);
    setResult(null);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  function changeMode(newMode: Mode) {
    setMode(newMode);
    clearAll();
  }

  function handleFile(file: File | null) {
    if (!file) return;

    setFile(file);
    setError("");

    if (file.type.startsWith("image/")) {
      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);
    } else {
      setPreview(null);
    }
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();

    const droppedFile = event.dataTransfer.files?.[0] ?? null;

    if (!droppedFile) return;

    if (mode === "image" && !droppedFile.type.startsWith("image/")) {
      setError("Please drop a PNG, JPG, or WEBP image.");
      return;
    }

    if (
      mode === "email" &&
      !droppedFile.name.toLowerCase().endsWith(".eml")
    ) {
      setError("Please drop an .eml email file.");
      return;
    }

    handleFile(droppedFile);
  }

  async function handleAnalyze() {
    if (mode === "text" && !text.trim()) return;
    if ((mode === "image" || mode === "email") && !file) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      let response: Response;

      if (mode === "text") {
        response = await fetch("http://127.0.0.1:8000/analyze", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: text.trim(),
          }),
        });
      } else {
        const formData = new FormData();
        formData.append("file", file as File);

        const endpoint =
          mode === "image"
            ? "http://127.0.0.1:8000/analyze-image"
            : "http://127.0.0.1:8000/analyze-email";

        response = await fetch(endpoint, {
          method: "POST",
          body: formData,
        });
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }

      setResult(data);
    } catch (err) {
      console.error(err);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to analyze the content."
      );
    } finally {
      setLoading(false);
    }
  }

  const confidence = result
    ? Math.round(result.confidence * 100)
    : 0;

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-10 text-white sm:px-6">
      <div className="mx-auto max-w-6xl">

        {/* Header */}
        <header className="mb-10 text-center">
          <div className="mb-4 text-6xl">🛡️</div>

          <h1 className="text-4xl font-bold tracking-tight md:text-6xl">
            Phish Guard AI
          </h1>

          <p className="mx-auto mt-4 max-w-3xl text-lg text-slate-400">
            AI-powered protection against phishing, scams,
            social engineering, and suspicious content.
          </p>
        </header>

        {/* Analyzer */}
        <section className="rounded-3xl border border-slate-800 bg-slate-900 p-5 shadow-2xl sm:p-7">

          {/* Mode selector */}
          <div className="mb-7 grid grid-cols-3 gap-2 rounded-2xl bg-slate-950 p-2">
            <button
              onClick={() => changeMode("text")}
              className={`rounded-xl px-3 py-3 text-sm font-semibold transition ${
                mode === "text"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "text-slate-400 hover:bg-slate-800"
              }`}
            >
              📝 Text / URL
            </button>

            <button
              onClick={() => changeMode("image")}
              className={`rounded-xl px-3 py-3 text-sm font-semibold transition ${
                mode === "image"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "text-slate-400 hover:bg-slate-800"
              }`}
            >
              📷 Screenshot
            </button>

            <button
              onClick={() => changeMode("email")}
              className={`rounded-xl px-3 py-3 text-sm font-semibold transition ${
                mode === "email"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "text-slate-400 hover:bg-slate-800"
              }`}
            >
              📧 Email
            </button>
          </div>

          {/* Text */}
          {mode === "text" && (
            <>
              <h2 className="text-xl font-semibold">
                Analyze suspicious content
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                Paste an email, SMS, WhatsApp message, or suspicious URL.
              </p>

              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                rows={10}
                placeholder="Paste a suspicious message here..."
                className="mt-5 w-full resize-none rounded-2xl border border-slate-700 bg-slate-950 p-4 text-white outline-none transition placeholder:text-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/10"
              />
            </>
          )}

          {/* Screenshot */}
          {mode === "image" && (
            <>
              <h2 className="text-xl font-semibold">
                Analyze a screenshot
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                Upload or drag and drop a suspicious screenshot.
              </p>

              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className="mt-5 cursor-pointer rounded-2xl border border-dashed border-slate-700 bg-slate-950 p-8 text-center transition hover:border-blue-500 hover:bg-slate-900"
              >
                {preview ? (
                  <div className="space-y-4">
                    <img
                      src={preview}
                      alt="Selected screenshot preview"
                      className="mx-auto max-h-80 rounded-xl object-contain shadow-xl"
                    />

                    <p className="text-sm text-slate-400">
                      Click or drop another image to replace it.
                    </p>
                  </div>
                ) : (
                  <>
                    <div className="text-5xl">📷</div>

                    <p className="mt-4 font-semibold">
                      Drop your screenshot here
                    </p>

                    <p className="mt-2 text-sm text-slate-500">
                      or click to choose a file
                    </p>

                    <p className="mt-3 text-xs text-slate-600">
                      PNG, JPG, WEBP
                    </p>
                  </>
                )}

                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/png,image/jpeg,image/webp"
                  onChange={(e) =>
                    handleFile(e.target.files?.[0] ?? null)
                  }
                  className="hidden"
                />
              </div>

              {file && (
                <div className="mt-4 flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950 p-4">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-white">
                      {file.name}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      clearAll();
                    }}
                    className="ml-4 rounded-lg px-3 py-2 text-sm text-slate-400 transition hover:bg-slate-800 hover:text-white"
                  >
                    Remove
                  </button>
                </div>
              )}
            </>
          )}

          {/* Email */}
          {mode === "email" && (
            <>
              <h2 className="text-xl font-semibold">
                Analyze an email file
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                Upload or drag and drop an .eml email file.
              </p>

              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className="mt-5 cursor-pointer rounded-2xl border border-dashed border-slate-700 bg-slate-950 p-10 text-center transition hover:border-blue-500 hover:bg-slate-900"
              >
                <div className="text-5xl">📧</div>

                <p className="mt-4 font-semibold">
                  Drop your .eml file here
                </p>

                <p className="mt-2 text-sm text-slate-500">
                  or click to choose a file
                </p>

                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".eml,message/rfc822"
                  onChange={(e) =>
                    handleFile(e.target.files?.[0] ?? null)
                  }
                  className="hidden"
                />
              </div>

              {file && (
                <div className="mt-4 flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950 p-4">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-white">
                      {file.name}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      clearAll();
                    }}
                    className="ml-4 rounded-lg px-3 py-2 text-sm text-slate-400 transition hover:bg-slate-800 hover:text-white"
                  >
                    Remove
                  </button>
                </div>
              )}
            </>
          )}

          {/* Actions */}
          <div className="mt-5 flex flex-col gap-3 sm:flex-row">
            <button
              onClick={handleAnalyze}
              disabled={
                loading ||
                (mode === "text" ? !text.trim() : !file)
              }
              className="flex-1 rounded-xl bg-blue-600 py-4 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading
                ? "Analyzing with AI..."
                : mode === "text"
                ? "Analyze Message"
                : mode === "image"
                ? "Analyze Screenshot"
                : "Analyze Email"}
            </button>

            <button
              type="button"
              onClick={clearAll}
              disabled={loading}
              className="rounded-xl border border-slate-700 px-6 py-4 font-semibold text-slate-300 transition hover:bg-slate-800 disabled:opacity-40"
            >
              Clear
            </button>
          </div>
        </section>

        {/* Error */}
        {error && (
          <div className="mt-6 rounded-2xl border border-red-800 bg-red-950/40 p-4 text-red-300">
            {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <section className="mt-8 space-y-6">

            {/* Risk summary */}
            <div
              className={`rounded-3xl border p-6 shadow-xl ${
                riskStyles[result.risk_level] ??
                riskStyles.MEDIUM
              }`}
            >
              <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] opacity-70">
                    Overall Risk
                  </p>

                  <div className="mt-2 flex items-center gap-3">
                    <span className="text-4xl">
                      {result.risk_level === "CRITICAL"
                        ? "🚨"
                        : result.risk_level === "HIGH"
                        ? "🔴"
                        : result.risk_level === "MEDIUM"
                        ? "🟠"
                        : "🟢"}
                    </span>

                    <h2 className="text-4xl font-bold">
                      {result.risk_level}
                    </h2>
                  </div>

                  <p className="mt-3 text-sm opacity-80">
                    {result.is_phishing
                      ? "Phishing or malicious activity detected."
                      : "No strong phishing indicators detected."}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="rounded-2xl bg-black/20 p-4 text-center">
                    <p className="text-xs uppercase tracking-wider opacity-60">
                      Risk Score
                    </p>

                    <p className="mt-1 text-3xl font-bold">
                      {result.risk_score}
                      <span className="text-base opacity-60">
                        /100
                      </span>
                    </p>
                  </div>

                  <div className="rounded-2xl bg-black/20 p-4 text-center">
                    <p className="text-xs uppercase tracking-wider opacity-60">
                      Confidence
                    </p>

                    <p className="mt-1 text-3xl font-bold">
                      {confidence}%
                    </p>
                  </div>
                </div>
              </div>

              <div className="mt-6">
                <div className="mb-2 flex justify-between text-xs opacity-70">
                  <span>Risk severity</span>
                  <span>{result.risk_score}/100</span>
                </div>

                <div className="h-3 overflow-hidden rounded-full bg-black/20">
                  <div
                    className="h-full rounded-full bg-current transition-all duration-700"
                    style={{
                      width: `${result.risk_score}%`,
                    }}
                  />
                </div>
              </div>
            </div>

            {/* Risk Score Breakdown */}
            {result.risk_breakdown && (
              <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h3 className="text-xl font-semibold">
                      Risk Score Breakdown
                    </h3>

                    <p className="mt-1 text-sm text-slate-500">
                      Transparent contribution of the detected security signals.
                    </p>
                  </div>

                  {result.risk_breakdown.capped && (
                    <span className="w-fit rounded-full bg-red-500/10 px-3 py-1 text-xs font-semibold text-red-400">
                      Score capped at 100
                    </span>
                  )}
                </div>

                <div className="mt-5 space-y-3">
                  {result.risk_breakdown.contributions.map(
                    (item, index) => (
                      <div
                        key={index}
                        className="flex flex-col gap-2 rounded-xl border border-slate-800 bg-slate-950 p-4 sm:flex-row sm:items-center sm:justify-between"
                      >
                        <div>
                          <p className="text-sm font-medium text-slate-200">
                            {item.signal}
                          </p>

                          <p className="mt-1 text-xs text-slate-500">
                            {item.source}
                          </p>
                        </div>

                        <span className="font-mono text-sm font-bold text-red-400">
                          +{item.points}
                        </span>
                      </div>
                    )
                  )}
                </div>

                <div className="mt-5 grid gap-3 sm:grid-cols-3">
                  <div className="rounded-xl bg-slate-950 p-4 text-center">
                    <p className="text-xs uppercase tracking-wider text-slate-500">
                      Raw Score
                    </p>

                    <p className="mt-1 text-2xl font-bold text-white">
                      {result.risk_breakdown.raw_score}
                    </p>
                  </div>

                  <div className="rounded-xl bg-slate-950 p-4 text-center">
                    <p className="text-xs uppercase tracking-wider text-slate-500">
                      Final Score
                    </p>

                    <p className="mt-1 text-2xl font-bold text-white">
                      {result.risk_breakdown.risk_score}/100
                    </p>
                  </div>

                  <div className="rounded-xl bg-slate-950 p-4 text-center">
                    <p className="text-xs uppercase tracking-wider text-slate-500">
                      Highest URL Risk
                    </p>

                    <p className="mt-1 text-2xl font-bold text-white">
                      {result.risk_breakdown.highest_url_score}/100
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Threats */}
            <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h3 className="text-xl font-semibold">
                    Threats Detected
                  </h3>

                  <p className="mt-1 text-sm text-slate-500">
                    Security indicators identified during analysis.
                  </p>
                </div>

                <span className="rounded-full bg-red-500/10 px-3 py-1 text-xs font-semibold text-red-400">
                  {result.threats.length} detected
                </span>
              </div>

              <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {result.threats.map((threat, index) => (
                  <div
                    key={index}
                    className="rounded-xl border border-red-500/20 bg-red-500/5 p-4"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-red-400">
                        ⚠
                      </span>

                      <span className="text-sm font-medium text-slate-200">
                        {threat}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Evidence */}
            <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="text-xl font-semibold">
                Evidence
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                Evidence supporting the security verdict.
              </p>

              <div className="mt-5 space-y-3">
                {result.evidence.map((item, index) => (
                  <div
                    key={index}
                    className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                  >
                    <div className="flex gap-3">
                      <span className="shrink-0 text-red-400">
                        ⚠
                      </span>

                      <p className="text-sm leading-6 text-slate-300">
                        {item}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Email Security Details */}
            {result.email_details && (
              <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
                <div>
                  <h3 className="text-xl font-semibold">
                    Email Security Details
                  </h3>

                  <p className="mt-1 text-sm text-slate-500">
                    Parsed email metadata and deterministic security checks.
                  </p>
                </div>

                <div className="mt-5 grid gap-4 md:grid-cols-2">
                  <div className="rounded-xl bg-slate-950 p-4">
                    <p className="text-xs uppercase tracking-wider text-slate-500">
                      Sender
                    </p>

                    <p className="mt-2 break-all text-sm text-white">
                      {result.email_details.sender_name
                        ? `${result.email_details.sender_name} <${result.email_details.sender_email}>`
                        : result.email_details.sender_email}
                    </p>
                  </div>

                  <div className="rounded-xl bg-slate-950 p-4">
                    <p className="text-xs uppercase tracking-wider text-slate-500">
                      Sender Domain
                    </p>

                    <p className="mt-2 break-all text-sm text-white">
                      {result.email_details.sender_domain || "Not available"}
                    </p>
                  </div>

                  <div className="rounded-xl bg-slate-950 p-4">
                    <p className="text-xs uppercase tracking-wider text-slate-500">
                      Reply-To
                    </p>

                    <p className="mt-2 break-all text-sm text-white">
                      {result.email_details.reply_email || "Not provided"}
                    </p>
                  </div>

                  <div className="rounded-xl bg-slate-950 p-4">
                    <p className="text-xs uppercase tracking-wider text-slate-500">
                      Reply-To Domain
                    </p>

                    <p className="mt-2 break-all text-sm text-white">
                      {result.email_details.reply_to_domain || "Not available"}
                    </p>
                  </div>

                  <div className="rounded-xl bg-slate-950 p-4 md:col-span-2">
                    <p className="text-xs uppercase tracking-wider text-slate-500">
                      Subject
                    </p>

                    <p className="mt-2 text-sm text-white">
                      {result.email_details.subject || "No subject"}
                    </p>
                  </div>
                </div>

                {result.email_details.security_flags.length > 0 && (
                  <div className="mt-5 rounded-xl border border-red-500/20 bg-red-500/5 p-4">
                    <p className="text-sm font-semibold text-red-400">
                      Security Flags
                    </p>

                    <div className="mt-3 space-y-2">
                      {result.email_details.security_flags.map(
                        (flag, index) => (
                          <p
                            key={index}
                            className="text-sm leading-6 text-slate-300"
                          >
                            ⚠ {flag}
                          </p>
                        )
                      )}
                    </div>
                  </div>
                )}

                {result.email_details.attachments.length > 0 && (
                  <div className="mt-5 rounded-xl border border-slate-800 bg-slate-950 p-4">
                    <div className="flex items-center justify-between gap-4">
                      <div>
                        <p className="text-sm font-semibold text-white">
                          Attachments
                        </p>
                        <p className="mt-1 text-xs text-slate-500">
                          Filename and file-type analysis only. Files are not opened or executed.
                        </p>
                      </div>

                      <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-400">
                        {result.email_details.attachments.length} file(s)
                      </span>
                    </div>

                    <div className="mt-4 space-y-3">
                      {result.email_details.attachment_analysis.length > 0
                        ? result.email_details.attachment_analysis.map(
                            (attachment, index) => (
                              <div
                                key={`${attachment.filename}-${index}`}
                                className="rounded-xl border border-slate-800 bg-slate-900 p-4"
                              >
                                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                                  <div className="min-w-0">
                                    <p className="break-all font-mono text-sm text-slate-200">
                                      📎 {attachment.filename}
                                    </p>
                                  </div>

                                  <div className="shrink-0 lg:text-right">
                                    <span
                                      className={`inline-flex rounded-full border px-3 py-1 text-xs font-bold ${
                                        riskStyles[attachment.risk_level] ??
                                        riskStyles.MEDIUM
                                      }`}
                                    >
                                      {attachment.risk_level}
                                    </span>

                                    <p className="mt-2 text-sm text-slate-400">
                                      {attachment.risk_score}/100
                                    </p>
                                  </div>
                                </div>

                                {attachment.reasons.length > 0 && (
                                  <div className="mt-4 space-y-2">
                                    {attachment.reasons.map((reason, reasonIndex) => (
                                      <p
                                        key={reasonIndex}
                                        className="text-sm text-slate-300"
                                      >
                                        • {reason}
                                      </p>
                                    ))}
                                  </div>
                                )}
                              </div>
                            )
                          )
                        : result.email_details.attachments.map(
                            (attachment, index) => (
                              <p
                                key={index}
                                className="text-sm text-slate-300"
                              >
                                📎 {attachment}
                              </p>
                            )
                          )}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* URL Analysis */}
            {result.urls.length > 0 && (
              <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
                <div>
                  <h3 className="text-xl font-semibold">
                    URL Analysis
                  </h3>

                  <p className="mt-1 text-sm text-slate-500">
                    URLs are analyzed structurally without opening them.
                  </p>
                </div>

                <div className="mt-5 space-y-4">
                  {result.urls.map((url, index) => (
                    <div
                      key={index}
                      className="rounded-2xl border border-slate-800 bg-slate-950 p-5"
                    >
                      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-start">

                        <div className="min-w-0">
                          <p className="break-all font-mono text-sm text-blue-400">
                            {url.url}
                          </p>

                          <p className="mt-2 text-sm text-slate-500">
                            Domain: {url.hostname}
                          </p>
                        </div>

                        <div className="lg:text-right">
                          <span
                            className={`inline-flex rounded-full border px-3 py-1 text-xs font-bold ${
                              riskStyles[url.risk_level] ??
                              riskStyles.MEDIUM
                            }`}
                          >
                            {url.risk_level}
                          </span>

                          <p className="mt-2 text-sm text-slate-400">
                            {url.risk_score}/100
                          </p>
                        </div>
                      </div>

                      {url.reasons.length > 0 && (
                        <div className="mt-4 rounded-xl border border-slate-800 bg-slate-900/50 p-4">
                          <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-500">
                            Signals
                          </p>

                          <div className="space-y-2">
                            {url.reasons.map((reason, i) => (
                              <p
                                key={i}
                                className="text-sm text-slate-300"
                              >
                                • {reason}
                              </p>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Recommendations */}
            <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="text-xl font-semibold">
                Recommended Actions
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                Practical actions to reduce your security risk.
              </p>

              <div className="mt-5 space-y-3">
                {result.recommendations.map((item, index) => (
                  <div
                    key={index}
                    className="rounded-xl border border-emerald-500/10 bg-emerald-500/5 p-4"
                  >
                    <div className="flex gap-3">
                      <span className="shrink-0 text-emerald-400">
                        ✓
                      </span>

                      <p className="text-sm leading-6 text-slate-300">
                        {item}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Disclaimer */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4 text-center text-xs leading-5 text-slate-500">
              Phish Guard AI provides automated security analysis.
              A LOW score does not guarantee that a message or URL is safe.
              Never share passwords, verification codes, or sensitive information
              with untrusted parties.
            </div>

          </section>
        )}
      </div>
    </main>
  );
}