export type URLAnalysis = {
  url: string;
  hostname: string;
  risk_score: number;
  risk_level: string;
  reasons: string[];
};

export type AttachmentAnalysis = {
  filename: string;
  risk_score: number;
  risk_level: string;
  reasons: string[];
};

export type EmailDetails = {
  sender_name: string;
  sender_email: string;
  sender_domain: string;
  reply_email: string;
  reply_to_domain: string;
  subject: string;
  attachments: string[];
  attachment_analysis: AttachmentAnalysis[];
  security_flags: string[];
};

export type RiskContribution = {
  signal: string;
  source: string;
  points: number;
};

export type RiskBreakdown = {
  raw_score: number;
  risk_score: number;
  risk_level: string;
  capped: boolean;
  highest_url_score: number;
  contributions: RiskContribution[];
};

export type AnalysisResult = {
  is_phishing: boolean;
  confidence: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  risk_score: number;
  threats: string[];
  evidence: string[];
  recommendations: string[];
  urls: URLAnalysis[];
  email_details: EmailDetails | null;
  risk_breakdown: RiskBreakdown | null;
};

/* ---- Trained domain model (POST /api/v1/detect) ---- */

export type Verdict = "PHISHING" | "SUSPICIOUS" | "LIKELY_SAFE" | "NOT_SCORED";

export type ModelInfo = {
  version?: string | null;
  trained_at?: string | null;
  model_name?: string | null;
  threshold?: number | null;
  threshold_review?: number | null;
  test_metrics?: {
    precision: number;
    recall: number;
    f1: number;
    fpr: number;
    roc_auc: number;
  } | null;
};

export type DetectResult = {
  url: string;
  host: string;
  scored_domain: string;
  probability: number | null;
  risk_score: number | null;
  verdict: Verdict;
  threshold: number | null;
  threshold_review: number | null;
  indicators: string[];
  model: ModelInfo;
};

export type DetectHealth = {
  status: "ok" | "model_missing";
  model?: ModelInfo;
  detail?: string;
};

/* ---- Private analysis (POST /api/v1/private/analyze) ---- */

export type PrivateSpan = { start: number; end: number; type: string; token: string };

export type PrivateAnalysis = {
  verdict: Verdict;
  risk_score: number;
  reasons: string[];
  recommendations: string[];
  violations: string[];
};

export type PrivateResult = {
  request_id: string;
  expires_in: number;
  provider: { name: string; model: string | null; status: string; detail: string | null };
  detection: { count: number; by_type: Record<string, number>; spans: PrivateSpan[] };
  sanitized_text: string;
  outbound: {
    fields: string[];
    bytes: number;
    sha256: string;
    forbidden_strings_checked: number;
    leak_check: string;
  };
  vault: { cipher: string; nonce_bits: number; kid: string; ciphertext_bytes: number; bound_to: string };
  custody: {
    scheme: string;
    threshold: number;
    total: number;
    kid: string;
    shares: { holder: string; share: string }[];
    note: string;
  };
  analysis: PrivateAnalysis | null;
  local: {
    status: string;
    risk_score: number;
    urls: { url: string; host: string; scored_domain: string; verdict: string; risk_score: number | null }[];
  };
  overall: { risk_score: number; source: string; level: "LOW" | "MEDIUM" | "HIGH" };
};

export type PrivateRestore = {
  restored: boolean;
  values_restored: number;
  reasons: string[];
  recommendations: string[];
};

export type SelfTest = {
  passed: number;
  total: number;
  checks: { name: string; passed: boolean; detail: string }[];
};
