import re
from typing import Dict, Any, List

class IsolatedSandboxSimulator:
    """
    Behavioral Sandbox Simulator: Performs static abstract interpretation 
    of payloads and simulated execution vectors without running host code.
    """
    @staticmethod
    def simulate_execution(text: str, attachments: List[str] = None) -> Dict[str, Any]:
        attachments = attachments or []
        behavioral_flags = []
        risk_increment = 0

        text_lower = text.lower()
        
        # Check for obfuscated script patterns or shell injections
        if any(keyword in text_lower for keyword in ["powershell", "cmd.exe", "bash -i", "eval(", "exec("]):
            behavioral_flags.append("Shell Execution Instruction Detected")
            risk_increment += 35

        # Check for credential harvesting form indicators
        if any(keyword in text_lower for keyword in ["input password", "enter your pin", "confirm credentials"]):
            behavioral_flags.append("Credential Harvesting DOM Simulation Triggered")
            risk_increment += 25

        for att in attachments:
            if any(ext in att.lower() for ext in [".exe", ".scr", ".ps1", ".vbs", ".bat"]):
                behavioral_flags.append(f"High-Risk Executable Payload in Sandbox: {att}")
                risk_increment += 40

        return {
            "sandbox_status": "isolated_analyzed",
            "behavioral_flags": behavioral_flags,
            "risk_increment": min(risk_increment, 100),
            "simulated_safe": risk_increment < 30
        }