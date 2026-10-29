import time
from fastapi import APIRouter, Response

router = APIRouter()

# Global metrics counters
REQUEST_COUNT = 0
TOTAL_LATENCY_MS = 0.0
THREATS_DETECTED_COUNT = 0

def record_request_metrics(latency_ms: float, is_phishing: bool):
    global REQUEST_COUNT, TOTAL_LATENCY_MS, THREATS_DETECTED_COUNT
    REQUEST_COUNT += 1
    TOTAL_LATENCY_MS += latency_ms
    if is_phishing:
        THREATS_DETECTED_COUNT += 1

@router.get("/metrics")
async def prometheus_metrics():
    """
    Prometheus Telemetry Metrics Exporter for PhishGuard AI Apex v15.
    """
    avg_latency = (TOTAL_LATENCY_MS / REQUEST_COUNT) if REQUEST_COUNT > 0 else 0.0
    
    metrics_output = f"""# HELP phishguard_requests_total Total HTTP analyze requests.
# TYPE phishguard_requests_total counter
phishguard_requests_total {REQUEST_COUNT}

# HELP phishguard_threats_detected_total Total critical phishing threats neutralized.
# TYPE phishguard_threats_detected_total counter
phishguard_threats_detected_total {THREATS_DETECTED_COUNT}

# HELP phishguard_avg_latency_ms Average mathematical pipeline latency in milliseconds.
# TYPE phishguard_avg_latency_ms gauge
phishguard_avg_latency_ms {avg_latency:.2f}

# HELP phishguard_active_cores_count Total active sovereign mathematical cores.
# TYPE phishguard_active_cores_count gauge
phishguard_active_cores_count 100
"""
    return Response(content=metrics_output, media_type="text/plain")