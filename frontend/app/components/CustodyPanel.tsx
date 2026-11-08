"use client";

import { useState } from "react";
import { restorePrivate } from "../lib/api";
import type { PrivateResult, PrivateRestore } from "../lib/types";
import { TokenText } from "./HighlightedText";

export default function CustodyPanel({ result }: { result: PrivateResult }) {
  const [chosen, setChosen] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [restored, setRestored] = useState<PrivateRestore | null>(null);
  const { threshold, total, shares } = result.custody;

  function toggle(holder: string) {
    setChosen((prev) => (prev.includes(holder) ? prev.filter((h) => h !== holder) : [...prev, holder]));
    setError("");
  }

  async function unlock() {
    setBusy(true);
    setError("");
    try {
      const picked = shares.filter((s) => chosen.includes(s.holder)).map((s) => s.share);
      setRestored(await restorePrivate(result.request_id, picked));
    } catch (err) {
      setRestored(null);
      setError(err instanceof Error ? err.message : "Could not unlock.");
    } finally {
      setBusy(false);
    }
  }

  const answer = result.analysis;

  return (
    <section className="rounded-lg border border-line bg-card p-6 sm:p-8">
      <h3 className="text-xl font-semibold">Unlock the protected values</h3>
      <p className="mt-1 max-w-2xl text-ink-2">
        The key that opens the vault is split into {total} shares. Any {threshold} of them unlock it; one alone reveals
        nothing. Gemini never receives any share.
      </p>

      <ul className="mt-5 grid gap-3 sm:grid-cols-3">
        {shares.map((s) => {
          const on = chosen.includes(s.holder);
          return (
            <li key={s.holder}>
              <button
                type="button"
                aria-pressed={on}
                onClick={() => toggle(s.holder)}
                className={`w-full rounded-md border-2 p-4 text-left transition-colors ${
                  on ? "border-accent bg-accent/5" : "border-line bg-paper hover:border-ink-2"
                }`}
              >
                <span className="flex items-center justify-between">
                  <span className="font-semibold">Holder {s.holder}</span>
                  <span className={`text-sm font-medium ${on ? "text-accent" : "text-ink-2"}`}>
                    {on ? "Included" : "Not included"}
                  </span>
                </span>
                <span className="mt-2 block break-all font-mono text-xs text-ink-2">{s.share.slice(0, 22)}...</span>
              </button>
            </li>
          );
        })}
      </ul>
      <p className="mt-2 text-sm text-ink-2">{result.custody.note}</p>

      <div className="mt-5 flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={unlock}
          disabled={busy || chosen.length === 0}
          className="rounded-md bg-accent px-6 py-3 font-semibold text-white transition-colors hover:bg-accent-hover disabled:cursor-not-allowed disabled:opacity-50"
        >
          {busy ? "Unlocking..." : `Unlock with ${chosen.length} ${chosen.length === 1 ? "holder" : "holders"}`}
        </button>
        <span className="text-sm text-ink-2">Try one holder first to see it refused, then add a second.</span>
      </div>

      <div aria-live="polite">
        {error && (
          <p role="alert" className="mt-4 rounded-md border border-danger/30 bg-danger-soft p-4 text-danger">
            {error}
          </p>
        )}
        {restored && (
          <div className="mt-5 rounded-md border border-safe/30 bg-safe-soft p-5">
            <p className="font-semibold text-safe">Unlocked. {restored.values_restored} protected values restored.</p>
            <p className="mt-1 text-sm text-ink-2">Done on this server, from the vault. Gemini never saw these.</p>
            {restored.reasons.length > 0 && (
              <ul className="mt-3 list-disc space-y-1.5 pl-5">
                {restored.reasons.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            )}
          </div>
        )}
        {!restored && answer && answer.reasons.length > 0 && (
          <div className="mt-5">
            <p className="text-sm font-medium text-ink-2">Gemini&apos;s reasons, still protected:</p>
            <ul className="mt-2 list-disc space-y-1.5 pl-5">
              {answer.reasons.map((r, i) => (
                <li key={i}>
                  <TokenText text={r} />
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </section>
  );
}
