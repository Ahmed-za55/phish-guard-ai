import type { RiskBreakdown } from "../lib/types";

/** Every point in the final score, listed like a receipt. */
export default function ScoreReceipt({ breakdown }: { breakdown: RiskBreakdown }) {
  return (
    <section className="rounded-lg border border-line bg-card p-6 sm:p-8">
      <h3 className="text-xl font-semibold">Where the score comes from</h3>
      <p className="mt-1 max-w-2xl text-ink-2">
        Each signal adds points. Nothing is hidden, and nothing is counted twice.
      </p>

      <ul className="mt-6 space-y-3">
        {breakdown.contributions.map((item, index) => (
          <li key={`${item.signal}-${index}`}>
            <div className="flex items-baseline gap-3">
              <span className="font-medium">{item.signal}</span>
              <span aria-hidden className="relative -top-1 min-w-4 flex-1 border-b border-dotted border-ink-2/40" />
              <span className="font-mono font-semibold">+{item.points}</span>
            </div>
            <span className="block text-sm text-ink-2">{item.source}</span>
          </li>
        ))}
        {breakdown.contributions.length === 0 && (
          <li className="text-ink-2">No signals added points.</li>
        )}
      </ul>

      <dl className="mt-6 space-y-2 border-t-2 border-ink pt-4">
        <div className="flex justify-between">
          <dt className="text-ink-2">Raw score</dt>
          <dd className="font-mono">{breakdown.raw_score}</dd>
        </div>
        {breakdown.capped && (
          <div className="flex justify-between">
            <dt className="text-ink-2">Capped at</dt>
            <dd className="font-mono">100</dd>
          </div>
        )}
        <div className="flex justify-between text-lg font-bold">
          <dt>Final score</dt>
          <dd className="font-mono">{breakdown.risk_score} / 100</dd>
        </div>
        <div className="flex justify-between text-sm">
          <dt className="text-ink-2">Highest single link</dt>
          <dd className="font-mono">{breakdown.highest_url_score} / 100</dd>
        </div>
      </dl>
    </section>
  );
}
