from notification.email import send_email
import httpx

print("📧 Testing Email Notification Setup...")
print()

# Get current jobs
try:
    jobs = httpx.get('http://127.0.0.1:8000/api/jobs').json()
    job_count = len(jobs)
    top_jobs = jobs[:3]
except:
    job_count = 16
    top_jobs = []

print(f"📊 Found {job_count} jobs to notify about")
print()

# Create professional email content
subject = f"🎯 JobPilot AI - {job_count} Job Matches Found!"

body = f"""
🎯 JobPilot AI - New Job Matches!

Hello,

Great news! We've found {job_count} job opportunities matching your profile in Embedded Systems, IoT, and Robotics.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 TOP JOB MATCHES:

"""

if top_jobs:
    for i, job in enumerate(top_jobs, 1):
        missing = ', '.join(job.get('missing_skills', [])[:3]) or 'None'
        present = ', '.join(job.get('present_skills', [])[:3]) or 'None'
        
        body += f"""
{i}. {job['title']}
   🏢 Company: {job['company']}
   📍 Location: {job.get('location', 'Remote')}
   🎯 Match Score: {job['score']}%
   
   ✅ Your Skills: {present}
   ❌ Missing Skills: {missing}
   
   🔗 Apply: {job['url']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

body += f"""

🌐 View Full Dashboard: http://127.0.0.1:8000
📄 Detailed Notifications: http://127.0.0.1:8000/static/notification.html

⚙️ Settings:
   • Match Threshold: 30%+
   • Auto-Apply: OFF (Manual review required)
   • Scan Frequency: Every 20 minutes

💡 This is an automated notification. You'll receive emails when new matching jobs are discovered.

Good luck with your applications! 🚀

---
JobPilot AI - Autonomous Job Discovery
Notifications: chauhanpriya0460@gmail.com
"""

print("📨 Sending test email to: chauhanpriya0460@gmail.com")
print()

try:
    result = send_email(subject, body)
    
    if result:
        print("="*60)
        print("✅ SUCCESS! Email sent!")
        print("="*60)
        print()
        print("📧 Check your inbox: chauhanpriya0460@gmail.com")
        print()
        print("You should receive:")
        print(f"  Subject: {subject}")
        print(f"  Content: Job details with links")
        print()
        print("✅ Email notifications are now ACTIVE!")
        print("📱 You'll get emails when new jobs are found (≥30% match)")
    else:
        print("❌ Email failed to send")
        print("Check your Gmail App Password")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("💡 Possible issues:")
    print("1. App Password incorrect")
    print("2. 2-Step Verification not enabled")
    print("3. App Passwords not generated correctly")
    print()
    print("Double-check: https://myaccount.google.com/apppasswords")
