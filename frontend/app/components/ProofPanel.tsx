"use client";

import { useState } from "react";
import { runSelfTest } from "../lib/api";
import type { PrivateResult, SelfTest } from "../lib/types";

export default function ProofPanel({ result }: { result: PrivateResult }) {
  const [test, setTest] = useState<SelfTest | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function run() {
    setBusy(true);
    setError("");
    try {
      setTest(await runSelfTest());
    } catch (err) {
      setError(err instanceof Error ? err.message : "The self-test could not run.");
    } finally {
      setBusy(false);
    }
  }

  const o = result.outbound;
  const rows: [string, string][] = [
    ["Sent to " + result.provider.name, `${o.bytes} bytes. Fields: ${o.fields.join(" and ")} only.`],
    ["Fingerprint of what was sent", `SHA-256 ${o.sha256.slice(0, 24)}...`],
    ["Sensitive values checked", `${o.forbidden_strings_checked} strings looked for in the outgoing text: leak check ${o.leak_check}.`],
    ["Vault", `${result.vault.cipher}, ${result.vault.nonce_bits}-bit nonce, tied to ${result.vault.bound_to}. Key id ${result.vault.kid}.`],
    ["Key custody", `${result.custody.scheme}, ${result.custody.threshold} of ${result.custody.total}.`],
    ["The key", "Generated per request, split into shares, and never persisted to disk or sent to the provider."],
    ["Provider answer", `Checked against a strict schema.${result.analysis && result.analysis.violations.length ? ` ${result.analysis.violations.length} issue(s) removed.` : " No issues found."}`],
  ];

  return (
    <section className="rounded-lg border border-line bg-card p-6 sm:p-8">
      <h3 className="text-xl font-semibold">What we can prove</h3>
      <dl className="mt-5 divide-y divide-line">
        {rows.map(([k, v]) => (
          <div key={k} className="grid gap-1 py-3 sm:grid-cols-[14rem_1fr] sm:gap-6">
            <dt className="text-ink-2">{k}</dt>
            <dd className="break-words">{v}</dd>
          </div>
        ))}
      </dl>

      <p className="mt-4 max-w-2xl text-sm text-ink-2">
        Limits: Gemini still reads every word that was not recognised as sensitive. This is tokenization with
        encrypted custody, not encrypted inference. Names the detector doesn&apos;t know need to be listed as protected words.
      </p>

      <div className="mt-6">
        <button
          type="button"
          onClick={run}
          disabled={busy}
          className="rounded-md border-2 border-ink px-5 py-2.5 font-semibold transition-colors hover:bg-ink hover:text-white disabled:opacity-50"
        >
          {busy ? "Running..." : "Run the security self-test"}
        </button>
        {error && <p role="alert" className="mt-3 text-danger">{error}</p>}
        {test && (
          <div className="mt-5" aria-live="polite">
            <p className="font-semibold">
              {test.passed} of {test.total} checks passed
            </p>
            <ul className="mt-3 space-y-2">
              {test.checks.map((c) => (
                <li key={c.name} className="flex gap-3">
                  <span
                    aria-label={c.passed ? "passed" : "failed"}
                    className={`mt-0.5 inline-flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs font-bold text-white ${
                      c.passed ? "bg-safe" : "bg-danger"
                    }`}
                  >
                    {c.passed ? "✓" : "×"}
                  </span>
                  <span>
                    <span className="font-medium">{c.name}</span>
                    <span className="block text-sm text-ink-2">{c.detail}</span>
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </section>
  );
}
