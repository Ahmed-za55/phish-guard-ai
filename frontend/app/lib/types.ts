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
