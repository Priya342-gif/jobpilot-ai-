import json
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from backend.config import settings
from backend.profile import PROFILE
from database.database import get_db, init_db
from database.models import Job, JobMatch, Application
from agents.matching_agent import match_job
from agents.skill_gap_agent import analyze_skill_gap

app = FastAPI(title=settings.app_name, version="0.1.0")

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def dashboard():
    return FileResponse(FRONTEND / "index.html")

@app.get("/api/health")
def health():
    return {
        "status": "running",
        "auto_apply": settings.auto_apply,
        "scan_interval_minutes": settings.scan_interval_minutes,
    }

@app.get("/api/profile")
def profile():
    return PROFILE

@app.get("/api/jobs")
def jobs(limit: int = 50, db: Session = Depends(get_db)):
    rows = (
        db.query(Job, JobMatch)
        .join(JobMatch, Job.id == JobMatch.job_id)
        .order_by(JobMatch.score.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "url": job.url,
            "source": job.source,
            "score": match.score,
            "missing_skills": json.loads(match.missing_skills or "[]"),
            "present_skills": json.loads(match.present_skills or "[]"),
            "recommendation": match.recommendation,
        }
        for job, match in rows
    ]

@app.get("/api/jobs/{job_id}/skill-gap")
def skill_gap(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")

    raw = {
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "required_skills": json.loads(job.required_skills or "[]"),
        "url": job.url,
    }

    return analyze_skill_gap(raw, PROFILE)

@app.get("/jobs/{job_id}/skill-analysis")
def skill_analysis_page(job_id: int):
    return FileResponse(FRONTEND / "skill-analysis.html")

@app.post("/api/demo/match")
def demo_match(job: dict):
    return match_job(job, PROFILE)

@app.get("/api/applications")
def applications(db: Session = Depends(get_db)):
    rows = db.query(Application).order_by(Application.id.desc()).all()
    return [
        {
            "id": row.id,
            "job_id": row.job_id,
            "status": row.status,
            "notes": row.notes,
            "submitted_at": row.submitted_at,
        }
        for row in rows
    ]
