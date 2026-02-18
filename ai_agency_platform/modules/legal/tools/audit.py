import datetime
from typing import Dict, Any

class AuditLogger:
    """
    Logs every step of the workflow with input/output snapshots for traceability.
    """

    def __init__(self):
        self.logs = []

    def log_step(self, step_name: str, input_snapshot: Any, output_snapshot: Any):
        """
        Records a log entry for a specific workflow step.
        """
        entry = {
            "step": step_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "input_snapshot": str(input_snapshot)[:200] + "...", # Truncate for log readability
            "output_snapshot": str(output_snapshot)[:200] + "..."
        }
        self.logs.append(entry)
        print(f"[AuditLogger] Logged step: {step_name}")
        
    def get_logs(self) -> list:
        return self.logs
