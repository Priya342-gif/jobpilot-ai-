from backend.config import settings

class ApplicationAgent:
    def __init__(self):
        self.enabled = settings.auto_apply

    def can_auto_apply(self, job: dict) -> bool:
        return bool(self.enabled and job.get("url"))

    def plan_application(self, job: dict, profile: dict) -> dict:
        return {
            "job": job.get("title", ""),
            "company": job.get("company", ""),
            "url": job.get("url", ""),
            "status": "planned",
            "auto_apply_enabled": self.enabled,
            "reason": (
                "Auto-apply is disabled by default. "
                "Enable only after reviewing application rules."
            ),
        }
