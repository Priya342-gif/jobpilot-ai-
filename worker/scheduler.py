import json
from apscheduler.schedulers.blocking import BlockingScheduler
from database.database import SessionLocal, init_db
from database.models import Job, JobMatch
from agents.job_search import discover_jobs
from agents.matching_agent import match_job
from agents.skill_gap_agent import analyze_skill_gap
from backend.profile import PROFILE
from backend.config import settings
from notification.email import send_email
from notification.whatsapp import send_whatsapp
import httpx as whatsapp_httpx

def save_and_analyze():
    print("[JobPilot] Starting scan...")

    db = SessionLocal()
    new_matches = []

    try:
        jobs = discover_jobs()

        for raw in jobs:
            external_id = raw.get("external_id") or raw["url"]

            existing = db.query(Job).filter(
                Job.external_id == external_id
            ).first()

            if existing:
                continue

            job = Job(
                external_id=external_id,
                title=raw.get("title", ""),
                company=raw.get("company", ""),
                location=raw.get("location", ""),
                url=raw.get("url", ""),
                description=raw.get("description", ""),
                required_skills=json.dumps(raw.get("required_skills", [])),
                source=raw.get("source", ""),
            )

            db.add(job)
            db.flush()

            result = match_job(raw, PROFILE)

            match = JobMatch(
                job_id=job.id,
                score=result["score"],
                present_skills=json.dumps(result["present_skills"]),
                missing_skills=json.dumps(result["missing_skills"]),
                recommendation=(
                    "strong_match"
                    if result["score"] >= settings.min_match_score
                    else "review"
                ),
            )

            db.add(match)

            if result["score"] >= settings.min_match_score:
                new_matches.append((raw, result))

        db.commit()

    finally:
        db.close()

    if new_matches:
        # Create professional email
        subject = f"🎯 JobPilot AI - {len(new_matches)} New Job Match{'es' if len(new_matches) > 1 else ''} Found!"
        
        body = f"""🎯 JobPilot AI - New Job Matches!

Hello,

Great news! We've found {len(new_matches)} new job opportunities matching your profile.

Your Profile: Embedded Systems, IoT, Robotics, Machine Learning
Match Threshold: {settings.min_match_score}%+

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEW JOB MATCHES:

"""
        
        for i, (job, result) in enumerate(new_matches[:10], 1):
            body += f"""{i}. {job.get('title')}
   🏢 Company: {job.get('company')}
   📍 Location: {job.get('location', 'Worldwide')}
   🎯 Match Score: {result['score']}%
   
   💼 Profile match based on keywords and domain relevance
   🔗 Apply: {job.get('url')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        body += f"""
🌐 View Full Dashboard: http://127.0.0.1:8000
📄 Detailed View: http://127.0.0.1:8000/static/notification.html

⚙️ Settings: Scan every 20 min | Threshold {settings.min_match_score}%+ | Auto-Apply OFF

Good luck with your applications! 🚀

---
JobPilot AI - Autonomous Job Discovery
"""
        
        send_email(subject, body)
        
        # Create notification HTML page
        try:
            import os
            html_content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>JobPilot - New Jobs</title>
<style>body{{font-family:Arial;background:#0b1020;color:#eef2ff;padding:20px}}.job{{background:#121a30;padding:15px;margin:15px 0;border-radius:10px}}.score{{color:#7ff0a9;font-weight:bold}}</style>
</head><body><h1>🎯 {len(new_matches)} New Job Matches!</h1>"""
            
            for job, result in new_matches:
                html_content += f"""<div class="job">
<h3>{job.get('title')}</h3>
<p>🏢 {job.get('company')} | <span class="score">Match: {result['score']}%</span></p>
<p>✅ Your skills: {', '.join(result['present_skills'][:3])}</p>
<p>❌ Missing: {', '.join(result['missing_skills'][:3]) or 'None'}</p>
<a href="{job.get('url')}" style="color:#8db8ff">Apply Now →</a></div>"""
            
            html_content += f"""<p><a href="http://127.0.0.1:8000" style="color:#8db8ff">View Full Dashboard →</a></p></body></html>"""
            
            frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
            with open(os.path.join(frontend_path, 'notification.html'), 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"[JobPilot] Notification page updated at /static/notification.html")
        except Exception as e:
            print(f"[JobPilot] Failed to create notification page: {e}")
        
        # Send WhatsApp template notification
        try:
            url = f"https://graph.facebook.com/v23.0/{settings.whatsapp_phone_number_id}/messages"
            headers = {
                "Authorization": f"Bearer {settings.whatsapp_access_token}",
                "Content-Type": "application/json",
            }
            
            # Send professional template
            payload = {
                "messaging_product": "whatsapp",
                "to": settings.whatsapp_to,
                "type": "template",
                "template": {
                    "name": "hello_world",
                    "language": {"code": "en_US"}
                }
            }
            response = whatsapp_httpx.post(url, headers=headers, json=payload, timeout=20)
            
            if response.status_code == 200:
                print(f"[JobPilot] WhatsApp notification sent for {len(new_matches)} new matches")
                print(f"[JobPilot] View details: http://127.0.0.1:8000/static/notification.html")
                
                # Try sending professional follow-up text
                import time
                time.sleep(2)
                
                professional_msg = f"""🎯 JobPilot AI Professional Alert

✅ {len(new_matches)} New Job Match{"es" if len(new_matches) > 1 else ""} Found!

Your profile in Embedded Systems, IoT & Robotics matches these opportunities.

📊 View Details:
http://127.0.0.1:8000/static/notification.html

🌐 Full Dashboard:
http://127.0.0.1:8000

Match Threshold: {settings.min_match_score}%+
Auto-Apply: OFF (Manual review required)

Good luck with your applications! 🚀"""
                
                text_payload = {
                    "messaging_product": "whatsapp",
                    "to": settings.whatsapp_to,
                    "type": "text",
                    "text": {"preview_url": True, "body": professional_msg}
                }
                
                try:
                    text_response = whatsapp_httpx.post(url, headers=headers, json=text_payload, timeout=20)
                    if text_response.status_code == 200:
                        print(f"[JobPilot] Professional message sent successfully")
                except:
                    pass  # Text might fail due to 24hr window restriction
                    
        except Exception as e:
            print(f"[JobPilot] WhatsApp notification failed: {e}")

    print(f"[JobPilot] Scan complete. New strong matches: {len(new_matches)}")

if __name__ == "__main__":
    init_db()

    scheduler = BlockingScheduler()
    scheduler.add_job(
        save_and_analyze,
        "interval",
        minutes=settings.scan_interval_minutes,
        max_instances=1,
        coalesce=True,
    )

    save_and_analyze()
    scheduler.start()
