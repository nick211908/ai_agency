from typing import Dict

class LegalEvaluator:
    """
    Evaluates the overall quality of the legal document based on multiple metrics.
    Q(y) = α * compliance + β * risk + γ * clarity + δ * completeness
    """

    def __init__(self, weights: Dict[str, float] = None):
        if weights is None:
            self.weights = {
                "compliance": 0.4,
                "risk": 0.3,
                "clarity": 0.15,
                "completeness": 0.15
            }
        else:
            self.weights = weights

    def evaluate(self, compliance_score: float, risk_score: float, clarity_score: float = 0.8, completeness_score: float = 0.8) -> float:
        """
        Calculates the weighted average score.
        Clarity and Completeness are mocked defaults for now.
        """
        print("[LegalEvaluator] Calculating overall quality score.")
        
        overall_score = (
            self.weights["compliance"] * compliance_score +
            self.weights["risk"] * risk_score +
            self.weights["clarity"] * clarity_score +
            self.weights["completeness"] * completeness_score
        )
        
        return round(overall_score, 2)
