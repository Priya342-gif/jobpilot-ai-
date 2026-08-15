import hashlib
import httpx
from backend.config import settings

class JobSource:
    name = "base"

    def fetch(self) -> list[dict]:
        raise NotImplementedError

class RemotiveSource(JobSource):
    name = "remotive"

    def fetch(self) -> list[dict]:
        response = httpx.get(settings.remotive_api_url, timeout=20)
        response.raise_for_status()
        data = response.json()

        jobs = []
        for item in data.get("jobs", []):
            jobs.append({
                "external_id": f"remotive:{item.get('id')}",
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("candidate_required_location", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "required_skills": [],
                "source": self.name,
            })
        return jobs

def make_external_id(url: str, title: str, company: str) -> str:
    raw = f"{url}|{title}|{company}".encode()
    return hashlib.sha256(raw).hexdigest()

def discover_jobs() -> list[dict]:
    sources = [RemotiveSource()]
    all_jobs = []

    for source in sources:
        try:
            all_jobs.extend(source.fetch())
        except Exception as exc:
            print(f"[JobPilot] source {source.name} failed: {exc}")

    return all_jobs
