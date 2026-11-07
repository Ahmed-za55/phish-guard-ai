import { LEVEL_TONE, TONE } from "../lib/format";
import type { AnalysisResult } from "../lib/types";
import ScoreReceipt from "./ScoreReceipt";

const card = "rounded-lg border border-line bg-card p-6 sm:p-8";

const LEVEL_COPY: Record<string, string> = {
  LOW: "No strong warning signs",
  MEDIUM: "Some warning signs",
  HIGH: "Likely phishing",
  CRITICAL: "Almost certainly phishing",
};

function Chip({ level }: { level: string }) {
  const tone = TONE[LEVEL_TONE[level] ?? "warn"];
  return (
    <span className={`inline-flex rounded-full border px-3 py-1 text-sm font-semibold ${tone.chip}`}>
      {level.charAt(0) + level.slice(1).toLowerCase()}
    </span>
  );
}

export default function AnalysisReport({ result }: { result: AnalysisResult }) {
  const tone = TONE[LEVEL_TONE[result.risk_level] ?? "warn"];
  const confidence = Math.round(result.confidence * 100);
  const email = result.email_details;

  return (
    <div className="space-y-6">
      {/* Verdict */}
      <article className={`rounded-lg border border-line border-l-[6px] ${tone.edge} bg-card p-6 sm:p-8`}>
        <Chip level={result.risk_level} />
        <h2 className="mt-4 text-3xl font-bold leading-tight sm:text-4xl">
          {LEVEL_COPY[result.risk_level] ?? result.risk_level}
        </h2>
        <p className="mt-3 max-w-2xl text-lg text-ink-2">
          {result.is_phishing
            ? "Phishing or other malicious activity was detected."
            : "Nothing here strongly suggests phishing. A low score is not a guarantee."}
        </p>

        <div className="mt-6 flex flex-wrap items-end gap-x-10 gap-y-4">
          <div>
            <p className="text-sm text-ink-2">Risk score</p>
            <p className="font-mono text-4xl font-bold">
              {result.risk_score}
              <span className="text-lg font-normal text-ink-2"> / 100</span>
            </p>
          </div>
          <div>
            <p className="text-sm text-ink-2">Confidence</p>
            <p className="font-mono text-4xl font-bold">{confidence}%</p>
          </div>
        </div>
        <div
          className="mt-5 h-3 overflow-hidden rounded-full bg-line"
          role="img"
          aria-label={`Risk score ${result.risk_score} out of 100`}
        >
          <div className={`h-full rounded-full ${tone.bar}`} style={{ width: `${result.risk_score}%` }} />
        </div>
      </article>

      {result.risk_breakdown && <ScoreReceipt breakdown={result.risk_breakdown} />}

      {/* Threats and evidence */}
      {(result.threats.length > 0 || result.evidence.length > 0) && (
        <section className={card}>
          {result.threats.length > 0 && (
            <>
              <h3 className="text-xl font-semibold">What was found</h3>
              <ul className="mt-4 flex flex-wrap gap-2">
                {result.threats.map((threat, i) => (
                  <li key={i} className="rounded-full border border-danger/30 bg-danger-soft px-3 py-1 text-sm font-medium text-danger">
                    {threat}
                  </li>
                ))}
              </ul>
            </>
          )}
          {result.evidence.length > 0 && (
            <>
              <h3 className={`text-xl font-semibold ${result.threats.length > 0 ? "mt-8" : ""}`}>Why</h3>
              <ul className="mt-4 space-y-3">
                {result.evidence.map((item, i) => (
                  <li key={i} className="flex gap-3">
                    <span aria-hidden className="mt-2.5 h-2 w-2 shrink-0 rounded-full bg-danger" />
                    <span className="max-w-3xl leading-7">{item}</span>
                  </li>
                ))}
              </ul>
            </>
          )}
        </section>
      )}

      {/* Links */}
      {result.urls.length > 0 && (
        <section className={card}>
          <h3 className="text-xl font-semibold">Links in this content</h3>
          <p className="mt-1 text-ink-2">Checked by their structure. None of them were opened.</p>
          <ul className="mt-6 divide-y divide-line">
            {result.urls.map((url, i) => (
              <li key={i} className="py-5 first:pt-0 last:pb-0">
                <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                  <div className="min-w-0">
                    <p className="break-all font-mono text-sm font-medium">{url.url}</p>
                    <p className="mt-1 text-sm text-ink-2">Domain: {url.hostname}</p>
                  </div>
                  <div className="flex items-center gap-3 sm:flex-col sm:items-end sm:gap-1">
                    <Chip level={url.risk_level} />
                    <span className="font-mono text-sm text-ink-2">{url.risk_score} / 100</span>
                  </div>
                </div>
                {url.reasons.length > 0 && (
                  <ul className="mt-3 space-y-1.5">
                    {url.reasons.map((reason, j) => {
                      const fromModel = reason.startsWith("Trained domain model");
                      return (
                        <li key={j} className="flex flex-wrap items-baseline gap-2 text-ink">
                          {fromModel && (
                            <span className="rounded border border-accent/30 bg-accent/10 px-1.5 py-0.5 text-xs font-semibold text-accent">
                              Trained model
                            </span>
                          )}
                          <span>{reason}</span>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Email */}
      {email && (
        <section className={card}>
          <h3 className="text-xl font-semibold">Email details</h3>
          <p className="mt-1 text-ink-2">Read from the headers. Attachments are never opened.</p>
          <dl className="mt-6 grid gap-x-8 gap-y-5 sm:grid-cols-2">
            <div>
              <dt className="text-sm text-ink-2">From</dt>
              <dd className="break-all">
                {email.sender_name ? `${email.sender_name} <${email.sender_email}>` : email.sender_email || "Not available"}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-ink-2">Sender domain</dt>
              <dd className="break-all font-mono text-sm">{email.sender_domain || "Not available"}</dd>
            </div>
            <div>
              <dt className="text-sm text-ink-2">Reply-To</dt>
              <dd className="break-all">{email.reply_email || "Not provided"}</dd>
            </div>
            <div>
              <dt className="text-sm text-ink-2">Reply-To domain</dt>
              <dd className="break-all font-mono text-sm">{email.reply_to_domain || "Not available"}</dd>
            </div>
            <div className="sm:col-span-2">
              <dt className="text-sm text-ink-2">Subject</dt>
              <dd>{email.subject || "No subject"}</dd>
            </div>
          </dl>

          {email.security_flags.length > 0 && (
            <div className="mt-6 rounded-md border border-danger/30 bg-danger-soft p-4">
              <p className="font-semibold text-danger">Header problems</p>
              <ul className="mt-2 list-disc space-y-1 pl-5">
                {email.security_flags.map((flag, i) => (
                  <li key={i}>{flag}</li>
                ))}
              </ul>
            </div>
          )}

          {email.attachments.length > 0 && (
            <div className="mt-6">
              <p className="font-semibold">Attachments ({email.attachments.length})</p>
              <ul className="mt-3 divide-y divide-line">
                {(email.attachment_analysis.length > 0
                  ? email.attachment_analysis
                  : email.attachments.map((filename) => ({ filename, risk_level: "", risk_score: 0, reasons: [] as string[] }))
                ).map((att, i) => (
                  <li key={`${att.filename}-${i}`} className="py-3">
                    <div className="flex items-start justify-between gap-4">
                      <p className="break-all font-mono text-sm">{att.filename}</p>
                      {att.risk_level && (
                        <div className="flex shrink-0 items-center gap-2">
                          <Chip level={att.risk_level} />
                          <span className="font-mono text-sm text-ink-2">{att.risk_score}</span>
                        </div>
                      )}
                    </div>
                    {att.reasons.length > 0 && (
                      <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-ink-2">
                        {att.reasons.map((reason, j) => (
                          <li key={j}>{reason}</li>
                        ))}
                      </ul>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}

      {/* Actions */}
      {result.recommendations.length > 0 && (
        <section className={card}>
          <h3 className="text-xl font-semibold">What to do</h3>
          <ul className="mt-4 space-y-3">
            {result.recommendations.map((item, i) => (
              <li key={i} className="flex gap-3">
                <span aria-hidden className="mt-2.5 h-2 w-2 shrink-0 rounded-full bg-safe" />
                <span className="max-w-3xl leading-7">{item}</span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
