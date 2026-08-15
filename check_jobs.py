import httpx

jobs = httpx.get('http://127.0.0.1:8000/api/jobs').json()

print(f"\n✅ WORKER IS WORKING!")
print(f"📊 Total jobs found: {len(jobs)}")
print(f"\n🎯 Top 5 Job Matches:\n")

for i, job in enumerate(jobs[:5], 1):
    print(f"{i}. {job['title']}")
    print(f"   Company: {job['company']}")
    print(f"   Match Score: {job['score']}%")
    print(f"   Location: {job['location']}")
    missing = job.get('missing_skills', [])
    if missing:
        print(f"   Missing Skills: {', '.join(missing[:3])}")
    print()

print(f"🌐 View all jobs: http://127.0.0.1:8000")
print(f"📚 API Docs: http://127.0.0.1:8000/docs")
