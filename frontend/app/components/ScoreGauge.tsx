import type { CSSProperties } from "react";

type Props = {
  score: number; // 0-100
  review: number | null; // 0-100, where "Suspicious" starts
  block: number | null; // 0-100, where "Likely phishing" starts
};

const clamp = (n: number) => Math.min(100, Math.max(0, n));

/** A 0-100 track split at the model's two decision thresholds, with a marker at the score. */
export default function ScoreGauge({ score, review, block }: Props) {
  const s = clamp(score);
  const r = review === null ? null : clamp(review);
  const b = block === null ? null : clamp(block);
  const reviewAt = r ?? b ?? 100;
  const blockAt = b ?? 100;

  return (
    <div className="mt-6">
      <div className="flex items-baseline justify-between">
        <p className="text-sm text-ink-2">Risk score</p>
        <p className="font-mono text-lg font-semibold">
          {score.toFixed(1)}
          <span className="text-sm font-normal text-ink-2"> / 100</span>
        </p>
      </div>

      <div
        className="relative mt-3 h-3 w-full overflow-visible rounded-full bg-line"
        role="img"
        aria-label={`Risk score ${score.toFixed(1)} out of 100`}
      >
        <div
          className="absolute inset-y-0 left-0 rounded-l-full bg-safe-soft ring-1 ring-inset ring-safe/30"
          style={{ width: `${reviewAt}%` }}
        />
        <div
          className="absolute inset-y-0 bg-warn-soft ring-1 ring-inset ring-warn/30"
          style={{ left: `${reviewAt}%`, width: `${Math.max(0, blockAt - reviewAt)}%` }}
        />
        <div
          className="absolute inset-y-0 right-0 rounded-r-full bg-danger-soft ring-1 ring-inset ring-danger/30"
          style={{ left: `${blockAt}%` }}
        />
        <div
          className="gauge-marker absolute -top-2 h-7 w-[3px] -translate-x-1/2 rounded-full bg-ink"
          style={{ "--to": `${s}%` } as CSSProperties}
        />
      </div>

      <div className="relative mt-2 h-5 text-xs text-ink-2">
        <span className="absolute left-0">0</span>
        {r !== null && (
          <span className="absolute -translate-x-1/2" style={{ left: `${r}%` }}>
            Suspicious from {r.toFixed(0)}
          </span>
        )}
        {b !== null && (
          <span className="absolute -translate-x-1/2" style={{ left: `${Math.min(b, 88)}%` }}>
            {b - (r ?? 0) < 18 ? "" : "Likely phishing from "}
            {b.toFixed(0)}
          </span>
        )}
        <span className="absolute right-0">100</span>
      </div>
    </div>
  );
}
