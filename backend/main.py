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

@app.post("/api/scan-jobs")
def scan_jobs_now(db: Session = Depends(get_db)):
    """Manually trigger job scanning"""
    try:
        from agents.job_search import search_jobs
        from agents.matching_agent import match_job
        from notification.email import send_email_notification
        from notification.whatsapp import send_whatsapp_notification
        import json
        
        # Search for jobs
        jobs = search_jobs()
        
        new_matches = []
        for job_data in jobs:
            # Check if already exists
            existing = db.query(Job).filter(Job.url == job_data["url"]).first()
            if existing:
                continue
            
            # Match job
            match_result = match_job(job_data, PROFILE)
            
            if match_result["score"] < settings.min_match_score:
                continue
            
            # Save job
            job = Job(
                title=job_data["title"],
                company=job_data["company"],
                location=job_data.get("location", "Remote"),
                description=job_data.get("description", ""),
                url=job_data["url"],
                source=job_data.get("source", "remotive"),
                required_skills=json.dumps(job_data.get("required_skills", [])),
            )
            db.add(job)
            db.flush()
            
            # Save match
            job_match = JobMatch(
                job_id=job.id,
                score=match_result["score"],
                missing_skills=json.dumps(match_result.get("missing_skills", [])),
                present_skills=json.dumps(match_result.get("present_skills", [])),
                recommendation=match_result.get("recommendation", ""),
            )
            db.add(job_match)
            new_matches.append((job, job_match))
        
        db.commit()
        
        # Send notifications if new matches found
        if new_matches and settings.notify_email_to:
            try:
                send_email_notification(new_matches, PROFILE)
            except:
                pass
        
        if new_matches and settings.whatsapp_to:
            try:
                send_whatsapp_notification(new_matches, PROFILE)
            except:
                pass
        
        return {
            "success": True,
            "jobs_found": len(jobs),
            "new_matches": len(new_matches),
            "message": f"Found {len(new_matches)} new job matches!"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

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
