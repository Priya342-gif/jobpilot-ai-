from notification.email import send_email
import httpx

print("📧 Sending improved email notification...")
print()

# Get current jobs
try:
    jobs = httpx.get('http://127.0.0.1:8000/api/jobs').json()
    job_count = len(jobs)
    top_jobs = jobs[:5]
except:
    job_count = 0
    top_jobs = []

subject = f"🎯 JobPilot AI - {job_count} Job Opportunities Found!"

body = f"""
🎯 JobPilot AI - New Job Matches!

Hello Priya,

Great news! We've found {job_count} remote job opportunities that match your profile.

Your Profile: Embedded Systems, IoT, Robotics, Machine Learning
Match Threshold: 30%+

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 TOP JOB MATCHES:

"""

if top_jobs:
    for i, job in enumerate(top_jobs, 1):
        body += f"""
{i}. {job['title']}
   🏢 Company: {job['company']}
   📍 Location: {job.get('location', 'Worldwide')}
   🎯 Match Score: {job['score']}%
   
   💼 Your profile matches this role based on:
      - Keywords in job description
      - Your skills: Python, C++, IoT, ML, Robotics
      - Target domains alignment
   
   🔗 Apply Now: {job['url']}
   
   📝 Tip: Read the full job description to see required skills!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

body += f"""

🌐 VIEW MORE:
   • Full Dashboard: http://127.0.0.1:8000
   • Detailed Notifications: http://127.0.0.1:8000/static/notification.html
   • API Docs: http://127.0.0.1:8000/docs

⚙️ SYSTEM INFO:
   • Scan Frequency: Every 20 minutes
   • Match Threshold: 30%+
   • Auto-Apply: OFF (Manual review required)
   • Total Jobs in Database: {job_count}

💡 HOW MATCHING WORKS:
   The system scans job descriptions for keywords related to:
   - Your skills (Python, C++, ESP32, TensorFlow, etc.)
   - Your target domains (Embedded Systems, IoT, Robotics, ML)
   - Match score = keyword matches + domain relevance

📌 NEXT STEPS:
   1. Click job links to read full descriptions
   2. Check if you meet the requirements
   3. Apply to jobs that match your experience
   4. Keep your profile updated as you learn new skills!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is an automated notification. You'll receive emails when new matching jobs are discovered every 20 minutes.

Good luck with your applications! 🚀

---
JobPilot AI - Autonomous Job Discovery
Email: chauhanpriya0460@gmail.com
WhatsApp: +91 8126394481
Dashboard: http://127.0.0.1:8000
"""

print(f"📨 Sending to: chauhanpriya0460@gmail.com")
print(f"📊 Jobs: {job_count}")
print()

try:
    result = send_email(subject, body)
    
    if result:
        print("="*60)
        print("✅ SUCCESS! Improved email sent!")
        print("="*60)
        print()
        print("📧 Check your inbox: chauhanpriya0460@gmail.com")
        print()
        print("This email includes:")
        print("  ✅ Top 5 job matches")
        print("  ✅ Match scores")
        print("  ✅ Direct apply links")
        print("  ✅ Explanation of matching system")
        print("  ✅ Clear action steps")
        print()
        print("No more 'None' - now shows what's being matched!")
    else:
        print("❌ Email failed")
        
except Exception as e:
    print(f"❌ Error: {e}")
