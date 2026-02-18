from typing import Dict, List

class RiskAnalyzer:
    """
    Analyzes legal documents for potential risks and vulnerabilities.
    """

    def analyze_risk(self, content: str) -> Dict:
        """
        Classifies the risk level and identifies specific vulnerabilities.
        """
        print("[RiskAnalyzer] Analyzing document for risks.")
        
        risks = []
        risk_level = "Low"
        
        # Simple keyword-based risk detection for MVP
        content_lower = content.lower()
        
        if "indemnify" not in content_lower:
            risks.append("Missing indemnification clause")
            risk_level = "Medium"
            
        if "liability" not in content_lower:
            risks.append("Missing limitation of liability")
            risk_level = "High"
            
        if "termination" not in content_lower:
            risks.append("Missing termination clause")
            if risk_level != "High":
                risk_level = "Medium"

        return {
            "risk_level": risk_level,
            "vulnerabilities": risks,
            "score": self._calculate_risk_score(risk_level)
        }

    def _calculate_risk_score(self, level: str) -> float:
        """
        Converts risk level to a normalized score (higher is better/safer).
        """
        if level == "Low":
            return 1.0
        elif level == "Medium":
            return 0.5
        else:
            return 0.0
