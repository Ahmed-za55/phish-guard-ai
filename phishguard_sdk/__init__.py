from backend.app.agents.orchestrator import ThreatOrchestrator

class PhishGuardSovereignSDK:
    """
    PhishGuard AI Official PyPI SDK:
    Enables external developers to invoke the 100+ sovereign cores and quantum-resilient 
    security pipelines in any Python application.
    """
    @staticmethod
    async def analyze(text: str):
        return await ThreatOrchestrator.analyze_concurrent(text)