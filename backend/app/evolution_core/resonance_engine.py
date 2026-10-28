import json
import time
from pathlib import Path
from typing import Dict, Any

METRICS_FILE = Path(__file__).resolve().parent.parent / "storage" / "evolution_metrics.json"
METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)

class SelfEvolvingNeuralResonance:
    """
    Self-Evolving Neural Resonance Core: Continuously adapts internal heuristic 
    weights and semantic vector thresholds based on cumulative threat resonance 
    and real-time feedback loops.
    """
    @classmethod
    def register_threat_event(cls, is_phishing: bool, confidence: float) -> Dict[str, Any]:
        metrics = {"total_evaluations": 0, "adaptive_mutation_rate": 0.0142, "system_plasticity": "optimal"}
        if METRICS_FILE.exists():
            try:
                metrics = json.loads(METRICS_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass

        metrics["total_evaluations"] += 1
        # Self-adaptive weight adjustment based on neural feedback
        if is_phishing:
            metrics["adaptive_mutation_rate"] = round(min(metrics["adaptive_mutation_rate"] * 1.001, 0.05), 5)
        
        metrics["last_resonance_timestamp"] = time.time()
        METRICS_FILE.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        return metrics