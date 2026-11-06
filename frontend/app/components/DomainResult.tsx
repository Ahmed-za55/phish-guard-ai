import { TONE, VERDICT_META } from "../lib/format";
import type { DetectResult } from "../lib/types";
import ScoreGauge from "./ScoreGauge";

export default function DomainResult({ result }: { result: DetectResult }) {
  const meta = VERDICT_META[result.verdict];
  const tone = TONE[meta.tone];
  const subdomainIgnored = result.host !== result.scored_domain;

  return (
    <article className={`rounded-lg border border-line border-l-[6px] ${tone.edge} bg-card p-6 sm:p-8`}>
      <p className={`inline-flex rounded-full border px-3 py-1 text-sm font-semibold ${tone.chip}`}>
        {meta.label}
      </p>
      <h2 className="mt-4 text-3xl font-bold leading-tight sm:text-4xl">{meta.headline}</h2>
      <p className="mt-3 max-w-2xl text-lg text-ink-2">{meta.body}</p>

      <p className="mt-6 text-sm text-ink-2">Domain that was scored</p>
      <p className="break-all font-mono text-lg font-medium">{result.scored_domain}</p>
      {subdomainIgnored && (
        <p className="mt-1 text-sm text-ink-2">
          Taken from <span className="font-mono">{result.host}</span>. Subdomains and paths are not scored.
        </p>
      )}

      {result.risk_score !== null && (
        <ScoreGauge
          score={result.risk_score}
          review={result.threshold_review !== null ? result.threshold_review * 100 : null}
          block={result.threshold !== null ? result.threshold * 100 : null}
        />
      )}

      <h3 className="mt-8 text-lg font-semibold">What stood out</h3>
      {result.indicators.length > 0 ? (
        <ul className="mt-3 space-y-2">
          {result.indicators.map((hint) => (
            <li key={hint} className="flex gap-3 text-ink">
              <span aria-hidden className={`mt-2 h-2 w-2 shrink-0 rounded-full ${tone.bar}`} />
              <span>{hint}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-2 text-ink-2">Nothing unusual in the name itself.</p>
      )}
      <p className="mt-4 max-w-2xl text-sm text-ink-2">
        These notes explain the input. The score comes only from the trained model.
      </p>
    </article>
  );
}
