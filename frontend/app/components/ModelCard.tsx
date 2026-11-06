import { modelDisplayName, percent } from "../lib/format";
import type { DetectHealth } from "../lib/types";

type Props = { health: DetectHealth | null; unreachable: boolean };

export default function ModelCard({ health, unreachable }: Props) {
  const metrics = health?.status === "ok" ? health.model?.test_metrics : null;

  return (
    <section aria-labelledby="accuracy-heading">
      <h2 id="accuracy-heading" className="text-2xl font-bold">
        How accurate is the domain check?
      </h2>

      {unreachable && (
        <p className="mt-4 max-w-2xl text-ink-2">
          The server isn&apos;t reachable, so the live numbers can&apos;t be shown. Start the backend and reload.
        </p>
      )}

      {health?.status === "model_missing" && (
        <p className="mt-4 max-w-2xl text-ink-2">
          No trained model is installed yet. Run <span className="font-mono text-sm">python scripts/train.py</span>{" "}
          in the backend folder, then reload.
        </p>
      )}

      {metrics && (
        <>
          <ul className="mt-5 max-w-2xl space-y-3 text-lg leading-7">
            <li>
              When the verdict is <strong>Likely phishing</strong>, it is right{" "}
              <strong className="font-mono">{percent(metrics.precision)}</strong> of the time.
            </li>
            <li>
              It catches <strong className="font-mono">{percent(metrics.recall)}</strong> of phishing domains.
            </li>
            <li>
              It wrongly flags <strong className="font-mono">{percent(metrics.fpr)}</strong> of legitimate domains.
            </li>
          </ul>
          <p className="mt-4 max-w-2xl text-ink-2">
            Measured on domains the model never saw during training. Model: {modelDisplayName(health?.model?.model_name)}
            {health?.model?.trained_at ? `, trained ${health.model.trained_at}` : ""}.
          </p>
        </>
      )}

      <h3 className="mt-8 text-lg font-semibold">What it can&apos;t do</h3>
      <ul className="mt-3 max-w-2xl list-disc space-y-2 pl-5 text-ink-2">
        <li>It reads the domain name only. It doesn&apos;t see the page, the path, the content or the domain&apos;s age.</li>
        <li>Sites on shared platforms such as github.io or netlify.app are not scored.</li>
        <li>
          Its test data holds popular and everyday domains. Real traffic is more varied, so expect more false alarms on small,
          unusual legitimate sites.
        </li>
      </ul>
    </section>
  );
}
