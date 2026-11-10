"use client";

import { useRef, useState } from "react";
import { analyzePrivately } from "../lib/api";
import { TONE } from "../lib/format";
import type { PrivateResult } from "../lib/types";
import CustodyPanel from "./CustodyPanel";
import { OriginalText, TYPE_LABEL, TokenText } from "./HighlightedText";
import ProofPanel from "./ProofPanel";

const SAMPLE =
  "Hello Mariam Hassan, we noticed unusual activity on your account. Your account will be locked within 24 hours unless you verify. " +
  "Confirm your details at http://secure-paypal-login-48213.xyz/verify and reply to support from mariam.hassan@example.org " +
  "or call +20 100 123 4567. Card on file: 4111 1111 1111 1111. Your verification code is 482913. password: Tr0ub4dor&3xx";

const LEVEL_COPY = {
  HIGH: { tone: "danger", headline: "Likely phishing" },
  MEDIUM: { tone: "warn", headline: "Suspicious" },
  LOW: { tone: "safe", headline: "No strong warning signs" },
} as const;

const primaryButton =
  "rounded-md bg-accent px-6 py-3 font-semibold text-white transition-colors hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-50";

const card = "rounded-lg border border-line bg-card p-6 sm:p-8";

function plural(count: number, type: string): string {
  const label = TYPE_LABEL[type] ?? type.toLowerCase();
  return `${count} ${label}${count === 1 ? "" : "s"}`;
}

export default function PrivateMode() {
  const [text, setText] = useState("");
  const [terms, setTerms] = useState("");
  const [sentText, setSentText] = useState("");
  const [result, setResult] = useState<PrivateResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const resultRef = useRef<HTMLDivElement>(null);

  async function analyze() {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const protectedTerms = terms.split(",").map((t) => t.trim()).filter(Boolean);
      const data = await analyzePrivately(text.trim(), protectedTerms);
      setSentText(text.trim());
      setResult(data);
      requestAnimationFrame(() => resultRef.current?.scrollIntoView({ block: "nearest", behavior: "smooth" }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  }

  const level = result ? LEVEL_COPY[result.overall.level] : null;
  const tone = level ? TONE[level.tone] : null;
  const mock = result?.provider.name === "mock";

  return (
    <div>
      <label htmlFor="private-input" className="block text-lg font-semibold">
        Paste a suspicious message, with your details left in
      </label>
      <p className="mt-1 max-w-2xl text-ink-2">
        Emails, phone numbers, card numbers, passwords and codes are swapped for random tokens before anything goes to
        Gemini. You can unlock them afterwards, here, with two of three key holders.
      </p>
      <textarea
        id="private-input"
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={7}
        placeholder="Paste the message here"
        className="mt-4 w-full resize-y rounded-md border border-line bg-paper p-4 text-base placeholder:text-ink-2/60 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/30"
      />
      <label htmlFor="private-terms" className="mt-4 block text-sm font-medium">
        Names or words to protect <span className="font-normal text-ink-2">(optional, separated by commas)</span>
      </label>
      <input
        id="private-terms"
        value={terms}
        onChange={(e) => setTerms(e.target.value)}
        placeholder="Mariam Hassan, Cairo Branch"
        className="mt-1 w-full rounded-md border border-line bg-paper px-4 py-3 text-base placeholder:text-ink-2/60 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/30"
      />
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <button type="button" onClick={analyze} disabled={loading || !text.trim()} className={primaryButton}>
          {loading ? "Protecting and analyzing..." : "Analyze privately"}
        </button>
        <button
          type="button"
          disabled={loading}
          onClick={() => {
            setText(SAMPLE);
            setTerms("Mariam Hassan");
          }}
          className="rounded-md px-3 py-3 text-sm font-medium text-accent hover:underline disabled:opacity-50"
        >
          Use a sample with personal details
        </button>
      </div>

      <div ref={resultRef} aria-live="polite" className="scroll-mt-6">
        {error && (
          <p role="alert" className="mt-6 rounded-lg border border-danger/30 bg-danger-soft p-5 text-danger">
            {error}
          </p>
        )}

        {result && level && tone && (
          <div className="mt-8 space-y-6">
            {mock && (
              <p className="rounded-md border border-warn/30 bg-warn-soft p-4 text-warn">
                Demo mode: no real AI model was called. Add a GEMINI_API_KEY to the backend to use Gemini.
              </p>
            )}

            {/* Before and after */}
            <section className={card}>
              <h3 className="text-xl font-semibold">What left this server</h3>
              <p className="mt-1 max-w-2xl text-ink-2">
                {result.provider.name === "gemini"
                  ? `Gemini${result.provider.model ? ` (${result.provider.model})` : ""} received only fixed instructions and the right-hand tokenized text.`
                  : "A provider would receive only fixed instructions and the right-hand tokenized text."}
              </p>
              <div className="mt-5 grid gap-4 lg:grid-cols-2">
                <div>
                  <p className="text-sm font-medium text-ink-2">What you wrote</p>
                  <p className="mt-2 whitespace-pre-wrap break-words rounded-md border border-line bg-paper p-4 leading-7">
                    <OriginalText text={sentText} spans={result.detection.spans} />
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-ink-2">What the provider received</p>
                  <p className="mt-2 whitespace-pre-wrap break-words rounded-md border border-line bg-paper p-4 leading-7">
                    <TokenText text={result.sanitized_text} />
                  </p>
                </div>
              </div>
              <p className="mt-4 text-ink-2">
                {result.detection.count === 0
                  ? "Nothing sensitive was recognised. The message was sent as written."
                  : `Replaced: ${Object.entries(result.detection.by_type)
                      .map(([type, n]) => plural(n, type))
                      .join(", ")}.`}
              </p>
            </section>

            {/* Verdict */}
            <article className={`rounded-lg border border-line border-l-[6px] ${tone.edge} bg-card p-6 sm:p-8`}>
              <p className={`inline-flex rounded-full border px-3 py-1 text-sm font-semibold ${tone.chip}`}>
                {result.overall.level.charAt(0) + result.overall.level.slice(1).toLowerCase()}
              </p>
              <h3 className="mt-4 text-3xl font-bold leading-tight sm:text-4xl">{level.headline}</h3>
              <dl className="mt-5 flex flex-wrap gap-x-10 gap-y-3">
                <div>
                  <dt className="text-sm text-ink-2">Local domain check</dt>
                  <dd className="font-mono text-2xl font-bold">
                    {result.local.status === "ok" ? Math.round(result.local.risk_score) : "n/a"}
                    <span className="text-base font-normal text-ink-2"> / 100</span>
                  </dd>
                </div>
                <div>
                  <dt className="text-sm text-ink-2">{mock ? "Demo model" : result.provider.name === "gemini" ? "Gemini" : result.provider.name}</dt>
                  <dd className="font-mono text-2xl font-bold">
                    {result.analysis ? result.analysis.risk_score : "n/a"}
                    <span className="text-base font-normal text-ink-2"> / 100</span>
                  </dd>
                </div>
              </dl>
              <p className="mt-3 text-sm text-ink-2">The headline uses the higher of the two scores.</p>

              {result.provider.status !== "ok" && (
                <p className="mt-4 rounded-md border border-warn/30 bg-warn-soft p-3 text-warn">
                  The AI provider did not answer ({result.provider.detail ?? result.provider.status}). Showing the local
                  results only.
                </p>
              )}

              {result.analysis && result.analysis.recommendations.length > 0 && (
                <>
                  <h4 className="mt-6 text-lg font-semibold">What to do</h4>
                  <ul className="mt-2 list-disc space-y-1.5 pl-5">
                    {result.analysis.recommendations.map((r, i) => (
                      <li key={i}>
                        <TokenText text={r} />
                      </li>
                    ))}
                  </ul>
                </>
              )}

              {result.local.urls.length > 0 && (
                <>
                  <h4 className="mt-6 text-lg font-semibold">Links checked on this server</h4>
                  <ul className="mt-2 divide-y divide-line">
                    {result.local.urls.map((u) => (
                      <li key={u.url} className="flex flex-wrap items-baseline justify-between gap-2 py-2">
                        <span className="break-all font-mono text-sm">{u.url}</span>
                        <span className="text-sm text-ink-2">
                          {u.verdict.replace("_", " ").toLowerCase()}
                          {u.risk_score !== null ? `, ${Math.round(u.risk_score)}/100` : ""}
                        </span>
                      </li>
                    ))}
                  </ul>
                </>
              )}
            </article>

            <CustodyPanel key={result.request_id} result={result} />
            <ProofPanel key={`proof-${result.request_id}`} result={result} />
          </div>
        )}
      </div>
    </div>
  );
}
