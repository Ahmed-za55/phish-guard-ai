import type { Verdict } from "./types";

export type Tone = "safe" | "warn" | "danger" | "muted";

// Full class names are written out so Tailwind can see them.
export const TONE: Record<
  Tone,
  { text: string; soft: string; edge: string; bar: string; chip: string }
> = {
  safe: {
    text: "text-safe",
    soft: "bg-safe-soft",
    edge: "border-l-safe",
    bar: "bg-safe",
    chip: "bg-safe-soft text-safe border-safe/30",
  },
  warn: {
    text: "text-warn",
    soft: "bg-warn-soft",
    edge: "border-l-warn",
    bar: "bg-warn",
    chip: "bg-warn-soft text-warn border-warn/30",
  },
  danger: {
    text: "text-danger",
    soft: "bg-danger-soft",
    edge: "border-l-danger",
    bar: "bg-danger",
    chip: "bg-danger-soft text-danger border-danger/30",
  },
  muted: {
    text: "text-ink-2",
    soft: "bg-paper",
    edge: "border-l-ink-2",
    bar: "bg-ink-2",
    chip: "bg-paper text-ink-2 border-line",
  },
};

export const VERDICT_META: Record<
  Verdict,
  { tone: Tone; label: string; headline: string; body: string }
> = {
  PHISHING: {
    tone: "danger",
    label: "Likely phishing",
    headline: "Don't open this link",
    body: "The domain name matches patterns seen in known phishing domains.",
  },
  SUSPICIOUS: {
    tone: "warn",
    label: "Suspicious",
    headline: "Be careful with this link",
    body: "Parts of this domain name resemble phishing domains. Check who sent it before you open it.",
  },
  LIKELY_SAFE: {
    tone: "safe",
    label: "No warning signs",
    headline: "No warning signs in the domain",
    body: "The domain name doesn't resemble known phishing domains. That is not a guarantee, so check the sender too.",
  },
  NOT_SCORED: {
    tone: "muted",
    label: "Not scored",
    headline: "The domain can't tell us about this site",
    body: "It is hosted on a shared platform, so the domain says nothing about this specific page.",
  },
};

export const LEVEL_TONE: Record<string, Tone> = {
  LOW: "safe",
  MEDIUM: "warn",
  HIGH: "danger",
  CRITICAL: "danger",
};

export function percent(value: number, digits = 1): string {
  return `${(value * 100).toFixed(digits)}%`;
}

export function modelDisplayName(name?: string | null): string {
  if (name === "logreg_ngrams_plus_features") return "Logistic regression on character patterns and name features";
  if (name === "random_forest_features_only") return "Random forest on name features";
  return name ?? "Trained classifier";
}
