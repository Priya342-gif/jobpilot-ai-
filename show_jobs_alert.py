import httpx
import webbrowser

# Get jobs from API
print("📊 Fetching your job matches...")
jobs = httpx.get('http://127.0.0.1:8000/api/jobs').json()

print(f"\n🎯 Found {len(jobs)} Jobs!")
print("="*50)

if jobs:
    print("\n🔥 Top 5 Job Matches:\n")
    for i, job in enumerate(jobs[:5], 1):
        print(f"{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Match Score: {job['score']}%")
        
        missing = job.get('missing_skills', [])
        if missing:
            print(f"   ❌ Missing Skills: {', '.join(missing[:3])}")
        
        present = job.get('present_skills', [])
        if present:
            print(f"   ✅ Your Skills: {', '.join(present[:3])}")
        
        print(f"   🔗 Apply: {job['url']}")
        print()

print("="*50)
print(f"\n🌐 Open dashboard to see all jobs:")
print("   http://127.0.0.1:8000")
print("\n📱 WhatsApp notifications will work once token is refreshed!")

# Ask if user wants to open dashboard
response = input("\n🚀 Open dashboard in browser? (y/n): ")
if response.lower() == 'y':
    webbrowser.open('http://127.0.0.1:8000')
    print("✅ Dashboard opened!")
