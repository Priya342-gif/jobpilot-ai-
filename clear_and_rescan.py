from database.database import SessionLocal
from database.models import Job, JobMatch
import httpx

print("🗑️ Clearing existing jobs from database...")

db = SessionLocal()
try:
    # Delete all job matches and jobs
    db.query(JobMatch).delete()
    db.query(Job).delete()
    db.commit()
    print("✅ Database cleared!")
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()

print("\n🔄 Triggering manual scan to find jobs again...")
print("This will simulate finding 'new' jobs and send WhatsApp notification!")
print("\nRunning job discovery...")

# Import and run the worker function
from worker.scheduler import save_and_analyze

save_and_analyze()

print("\n✅ Scan complete!")
print("📱 Check your WhatsApp for notification!")
print("🌐 View jobs: http://127.0.0.1:8000")
