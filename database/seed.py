import json
from database.database import SessionLocal, init_db
from database.models import Job, JobMatch
from agents.matching_agent import match_job
from backend.profile import PROFILE

DEMO_JOBS = [
    {
        "external_id": "demo-embedded-001",
        "title": "Embedded Systems Intern",
        "company": "Demo Robotics",
        "location": "Bangalore",
        "url": "https://example.com/embedded-intern",
        "description": "Embedded C C++ STM32 UART SPI I2C FreeRTOS CAN firmware robotics",
        "required_skills": ["C", "C++", "STM32", "UART", "SPI", "FreeRTOS", "CAN"],
        "source": "demo",
    },
    {
        "external_id": "demo-ml-001",
        "title": "Machine Learning Intern",
        "company": "Demo AI",
        "location": "Remote",
        "url": "https://example.com/ml-intern",
        "description": "Python TensorFlow Keras scikit-learn machine learning",
        "required_skills": ["Python", "TensorFlow", "Keras", "Scikit-learn"],
        "source": "demo",
    },
]

init_db()
db = SessionLocal()

for raw in DEMO_JOBS:
    if db.query(Job).filter(Job.external_id == raw["external_id"]).first():
        continue

    job = Job(
        external_id=raw["external_id"],
        title=raw["title"],
        company=raw["company"],
        location=raw["location"],
        url=raw["url"],
        description=raw["description"],
        required_skills=json.dumps(raw["required_skills"]),
        source=raw["source"],
    )
    db.add(job)
    db.flush()

    result = match_job(raw, PROFILE)
    db.add(JobMatch(
        job_id=job.id,
        score=result["score"],
        present_skills=json.dumps(result["present_skills"]),
        missing_skills=json.dumps(result["missing_skills"]),
        recommendation="strong_match" if result["score"] >= 70 else "review",
    ))

db.commit()
db.close()
print("Demo jobs inserted.")
