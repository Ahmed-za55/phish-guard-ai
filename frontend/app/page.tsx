"use client";

import { FormEvent, KeyboardEvent, useEffect, useRef, useState } from "react";
import AnalysisReport from "./components/AnalysisReport";
import DomainResult from "./components/DomainResult";
import DropZone from "./components/DropZone";
import ModelCard from "./components/ModelCard";
import { analyzeFile, analyzeText, detectDomain, fetchModelHealth } from "./lib/api";
import type { AnalysisResult, DetectHealth, DetectResult } from "./lib/types";

type Mode = "domain" | "text" | "image" | "email";
type Result =
  | { kind: "domain"; data: DetectResult }
  | { kind: "report"; data: AnalysisResult };

const TABS: { id: Mode; label: string }[] = [
  { id: "domain", label: "Link or domain" },
  { id: "text", label: "Message" },
  { id: "image", label: "Screenshot" },
  { id: "email", label: "Email file" },
];

const DOMAIN_EXAMPLES = [
  { label: "en.wikipedia.org", value: "https://en.wikipedia.org/wiki/Egypt" },
  { label: "secure-paypal-login-48213.xyz", value: "http://secure-paypal-login-48213.xyz/verify" },
  { label: "paypal.com.account-verify.top", value: "https://paypal.com.account-verify.top/login" },
  { label: "my-site.netlify.app", value: "https://my-site.netlify.app" },
];

const SAMPLE_MESSAGE =
  "Your account has been suspended. Verify your identity within 24 hours to avoid permanent closure: http://secure-paypal-login-48213.xyz/verify";

const primaryButton =
  "rounded-md bg-accent px-6 py-3 font-semibold text-white transition-colors hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-50";

export default function Home() {
  const [mode, setMode] = useState<Mode>("domain");
  const [domain, setDomain] = useState("");
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [health, setHealth] = useState<DetectHealth | null>(null);
  const [unreachable, setUnreachable] = useState(false);

  const previewUrl = useRef<string | null>(null);
  const resultRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchModelHealth()
      .then(setHealth)
      .catch(() => setUnreachable(true));
    return () => {
      if (previewUrl.current) URL.revokeObjectURL(previewUrl.current);
    };
  }, []);

  useEffect(() => {
    if (result) resultRef.current?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }, [result]);

  function clearFile() {
    if (previewUrl.current) URL.revokeObjectURL(previewUrl.current);
    previewUrl.current = null;
    setFile(null);
    setPreview(null);
  }

  function changeMode(next: Mode) {
    if (next === mode) return;
    setMode(next);
    clearFile();
    setResult(null);
    setError("");
  }

  function onTabKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    const index = TABS.findIndex((t) => t.id === mode);
    let next = index;
    if (event.key === "ArrowRight") next = (index + 1) % TABS.length;
    else if (event.key === "ArrowLeft") next = (index - 1 + TABS.length) % TABS.length;
    else return;
    event.preventDefault();
    changeMode(TABS[next].id);
    document.getElementById(`tab-${TABS[next].id}`)?.focus();
  }

  function pickFile(picked: File) {
    clearFile();
    setFile(picked);
    setError("");
    setResult(null);
    if (picked.type.startsWith("image/")) {
      const url = URL.createObjectURL(picked);
      previewUrl.current = url;
      setPreview(url);
    }
  }

  async function run(task: () => Promise<Result>) {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      setResult(await task());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  }

  function checkDomain(value: string) {
    const trimmed = value.trim();
    if (!trimmed) return;
    run(async () => ({ kind: "domain", data: await detectDomain(trimmed) }));
  }

  function onDomainSubmit(event: FormEvent) {
    event.preventDefault();
    checkDomain(domain);
  }

  function analyzeCurrent() {
    if (mode === "text" && text.trim()) {
      run(async () => ({ kind: "report", data: await analyzeText(text.trim()) }));
    } else if ((mode === "image" || mode === "email") && file) {
      run(async () => ({ kind: "report", data: await analyzeFile(mode, file) }));
    }
  }

  const canAnalyze = mode === "text" ? Boolean(text.trim()) : Boolean(file);

  return (
    <>
      <header className="mx-auto flex w-full max-w-5xl items-center justify-between px-5 py-6">
        <div className="flex items-center gap-2.5">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden className="text-accent">
            <path d="M12 2.5 4.5 5.5v6c0 4.6 3.1 8.2 7.5 10 4.4-1.8 7.5-5.4 7.5-10v-6L12 2.5Z" fill="currentColor" fillOpacity=".12" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
            <path d="m8.8 12.2 2.3 2.3 4.2-4.6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <span className="text-lg font-bold tracking-tight">Phish Guard AI</span>
        </div>
        <a
          href="https://github.com/Ahmed-za55/phish-guard-ai"
          className="text-sm font-medium text-ink-2 underline-offset-4 hover:text-ink hover:underline"
        >
          Source on GitHub
        </a>
      </header>

      <main className="mx-auto w-full max-w-5xl flex-1 px-5 pb-20">
        <section className="pt-8 sm:pt-14">
          <h1 className="max-w-4xl text-balance text-4xl font-bold leading-[1.1] tracking-tight sm:text-6xl">
            Check it before you click.
          </h1>
          <p className="mt-5 max-w-2xl text-lg text-ink-2 sm:text-xl">
            Paste a link, a message, a screenshot or an email. You get a verdict and every reason behind it.
          </p>
        </section>

        {/* Tool */}
        <section className="mt-10 rounded-xl border border-line bg-card p-5 shadow-sm sm:p-8" aria-label="Checker">
          <div
            role="tablist"
            aria-label="What to check"
            onKeyDown={onTabKeyDown}
            className="flex flex-wrap gap-x-7 gap-y-1 border-b border-line"
          >
            {TABS.map((tab) => {
              const selected = tab.id === mode;
              return (
                <button
                  key={tab.id}
                  id={`tab-${tab.id}`}
                  role="tab"
                  type="button"
                  aria-selected={selected}
                  aria-controls="tool-panel"
                  tabIndex={selected ? 0 : -1}
                  onClick={() => changeMode(tab.id)}
                  className={`-mb-px border-b-[3px] pb-3 pt-1 text-base font-semibold transition-colors ${
                    selected ? "border-accent text-ink" : "border-transparent text-ink-2 hover:text-ink"
                  }`}
                >
                  {tab.label}
                </button>
              );
            })}
          </div>

          <div id="tool-panel" role="tabpanel" aria-labelledby={`tab-${mode}`} className="pt-6">
            {mode === "domain" && (
              <form onSubmit={onDomainSubmit}>
                <label htmlFor="domain-input" className="block text-lg font-semibold">
                  Paste a link or domain
                </label>
                <p className="mt-1 text-ink-2">
                  Scored by a trained model. It runs on our server and nothing is opened.
                </p>
                <div className="mt-4 flex flex-col gap-3 sm:flex-row">
                  <input
                    id="domain-input"
                    type="text"
                    inputMode="url"
                    autoComplete="off"
                    spellCheck={false}
                    value={domain}
                    onChange={(e) => setDomain(e.target.value)}
                    placeholder="https://example.com/login"
                    className="min-w-0 flex-1 rounded-md border border-line bg-paper px-4 py-3 font-mono text-base placeholder:text-ink-2/60 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/30"
                  />
                  <button type="submit" disabled={loading || !domain.trim()} className={primaryButton}>
                    {loading ? "Checking..." : "Check link"}
                  </button>
                </div>
                <div className="mt-4 flex flex-wrap items-center gap-2">
                  <span className="text-sm text-ink-2">Try one:</span>
                  {DOMAIN_EXAMPLES.map((ex) => (
                    <button
                      key={ex.label}
                      type="button"
                      disabled={loading}
                      onClick={() => {
                        setDomain(ex.value);
                        checkDomain(ex.value);
                      }}
                      className="rounded-full border border-line bg-paper px-3 py-1.5 font-mono text-xs text-ink hover:border-accent disabled:opacity-50"
                    >
                      {ex.label}
                    </button>
                  ))}
                </div>
              </form>
            )}

            {mode === "text" && (
              <div>
                <label htmlFor="message-input" className="block text-lg font-semibold">
                  Paste a message
                </label>
                <p className="mt-1 text-ink-2">An email, SMS or WhatsApp text. Links inside it are checked too.</p>
                <textarea
                  id="message-input"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  rows={8}
                  placeholder="Paste the message here"
                  className="mt-4 w-full resize-y rounded-md border border-line bg-paper p-4 text-base placeholder:text-ink-2/60 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/30"
                />
                <div className="mt-4 flex flex-wrap items-center gap-3">
                  <button type="button" onClick={analyzeCurrent} disabled={loading || !canAnalyze} className={primaryButton}>
                    {loading ? "Analyzing..." : "Analyze message"}
                  </button>
                  <button
                    type="button"
                    onClick={() => setText(SAMPLE_MESSAGE)}
                    disabled={loading}
                    className="rounded-md px-3 py-3 text-sm font-medium text-accent hover:underline disabled:opacity-50"
                  >
                    Use a sample phishing message
                  </button>
                </div>
              </div>
            )}

            {(mode === "image" || mode === "email") && (
              <div>
                <h2 className="text-lg font-semibold">
                  {mode === "image" ? "Upload a screenshot" : "Upload an email file"}
                </h2>
                <p className="mb-4 mt-1 text-ink-2">
                  {mode === "image"
                    ? "A vision model reads the screenshot, and any links in it are checked."
                    : "The headers, links and attachment names are checked. Nothing is opened or run."}
                </p>
                <DropZone
                  key={mode}
                  kind={mode}
                  file={file}
                  preview={preview}
                  onFile={pickFile}
                  onInvalid={setError}
                  onRemove={() => {
                    clearFile();
                    setResult(null);
                  }}
                />
                <button type="button" onClick={analyzeCurrent} disabled={loading || !canAnalyze} className={`mt-4 ${primaryButton}`}>
                  {loading ? "Analyzing..." : mode === "image" ? "Analyze screenshot" : "Analyze email"}
                </button>
              </div>
            )}
          </div>
        </section>

        {/* Results */}
        <div ref={resultRef} aria-live="polite" className="mt-8 scroll-mt-6">
          {error && (
            <div role="alert" className="rounded-lg border border-danger/30 bg-danger-soft p-5 text-danger">
              {error}
            </div>
          )}
          {result?.kind === "domain" && <DomainResult result={result.data} />}
          {result?.kind === "report" && <AnalysisReport result={result.data} />}
        </div>

        {/* How a verdict is built */}
        <section className="mt-20" aria-labelledby="built-heading">
          <h2 id="built-heading" className="text-2xl font-bold">
            How a verdict is built
          </h2>
          <div className="mt-6 grid gap-8 md:grid-cols-3 md:gap-0 md:divide-x md:divide-line">
            <div className="md:pr-8">
              <h3 className="text-lg font-semibold">Trained domain model</h3>
              <p className="mt-2 text-ink-2">
                A classifier trained on public lists of phishing and legitimate domains judges the name of the site.
              </p>
            </div>
            <div className="md:px-8">
              <h3 className="text-lg font-semibold">Rule checks</h3>
              <p className="mt-2 text-ink-2">
                Entropy, look-alike spellings, link shorteners and email header mismatches. Each rule adds points you can see in the score.
              </p>
            </div>
            <div className="md:pl-8">
              <h3 className="text-lg font-semibold">Language model</h3>
              <p className="mt-2 text-ink-2">
                Gemini reads message text and screenshots for pressure tactics and impersonation. For messages and emails, the other two still run if it is unavailable. Screenshots need it.
              </p>
            </div>
          </div>
        </section>

        <div className="mt-20 border-t border-line pt-12">
          <ModelCard health={health} unreachable={unreachable} />
        </div>
      </main>

      <footer className="mx-auto w-full max-w-5xl px-5 pb-10 text-sm text-ink-2">
        Built for the AI Builders Hackathon 2026. A low score does not guarantee a message is safe. Never share passwords or
        verification codes with anyone you don&apos;t trust.
      </footer>
    </>
  );
}

