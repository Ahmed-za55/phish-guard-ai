import type { PrivateSpan } from "../lib/types";

export const TYPE_LABEL: Record<string, string> = {
  EMAIL: "email address",
  PHONE: "phone number",
  CARD: "card number",
  IBAN: "IBAN",
  NATIONAL_ID: "national ID",
  SSN: "SSN",
  SECRET: "secret or password",
  CODE: "one-time code",
  PROTECTED: "protected word",
};

const TOKEN_SPLIT = /(\[\[[A-Za-z_]+_\d+_[a-z0-9]{4}\]\])/;

/** Text where tokens (what the provider sees) are drawn as chips. */
export function TokenText({ text }: { text: string }) {
  return (
    <>
      {text.split(TOKEN_SPLIT).map((part, i) =>
        i % 2 === 1 ? (
          <span
            key={i}
            className="mx-0.5 inline-block rounded border border-accent/30 bg-accent/10 px-1.5 py-px font-mono text-[0.8em] font-medium text-accent"
          >
            {part}
          </span>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </>
  );
}

/** The original text with each protected value underlined. */
export function OriginalText({ text, spans }: { text: string; spans: PrivateSpan[] }) {
  const ordered = [...spans].sort((a, b) => a.start - b.start);
  const parts: React.ReactNode[] = [];
  let cursor = 0;
  ordered.forEach((span, i) => {
    if (span.start < cursor) return;
    if (span.start > cursor) parts.push(<span key={`t${i}`}>{text.slice(cursor, span.start)}</span>);
    parts.push(
      <mark
        key={`m${i}`}
        title={TYPE_LABEL[span.type] ?? span.type}
        className="rounded-sm border-b-2 border-warn bg-warn-soft px-0.5 text-ink"
      >
        {text.slice(span.start, span.end)}
      </mark>
    );
    cursor = span.end;
  });
  if (cursor < text.length) parts.push(<span key="tail">{text.slice(cursor)}</span>);
  return <>{parts}</>;
}
