import httpx
import json
from datetime import datetime

# Get current jobs
try:
    jobs = httpx.get('http://127.0.0.1:8000/api/jobs').json()
except:
    jobs = []

# Create HTML notification page
html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>JobPilot AI - Job Notification</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #0b1020;
            color: #eef2ff;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: #121a30;
            border-radius: 15px;
            padding: 25px;
            border: 1px solid #263250;
        }}
        h1 {{
            color: #7ff0a9;
            margin-top: 0;
        }}
        .job {{
            background: #1a2340;
            padding: 15px;
            margin: 15px 0;
            border-radius: 10px;
            border-left: 4px solid #3b82f6;
        }}
        .job-title {{
            font-size: 18px;
            font-weight: bold;
            color: #8db8ff;
            margin-bottom: 8px;
        }}
        .company {{
            color: #9aa7c2;
            font-size: 14px;
            margin-bottom: 5px;
        }}
        .score {{
            background: #153d2b;
            color: #7ff0a9;
            padding: 5px 12px;
            border-radius: 20px;
            display: inline-block;
            font-size: 14px;
            font-weight: bold;
            margin: 8px 0;
        }}
        .skills {{
            margin: 10px 0;
        }}
        .tag {{
            background: #202b47;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 12px;
            display: inline-block;
            margin: 3px;
        }}
        .missing {{
            background: #47252c;
            color: #ffabb6;
        }}
        .apply-btn {{
            background: #3b82f6;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin-top: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #9aa7c2;
            font-size: 13px;
        }}
        .dashboard-link {{
            background: #2d3748;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-top: 20px;
        }}
        .dashboard-link a {{
            color: #8db8ff;
            text-decoration: none;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 JobPilot AI Notification</h1>
        <p style="color: #9aa7c2;">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <p><strong>Total Jobs Found: {len(jobs)}</strong></p>
        
        <div class="dashboard-link">
            <a href="http://127.0.0.1:8000">🌐 Open Full Dashboard</a>
        </div>
"""

if jobs:
    html += "<h2>🔥 Top Job Matches:</h2>"
    for i, job in enumerate(jobs[:5], 1):
        missing = job.get('missing_skills', [])
        present = job.get('present_skills', [])
        
        html += f"""
        <div class="job">
            <div class="job-title">{i}. {job['title']}</div>
            <div class="company">🏢 {job['company']} · 📍 {job.get('location', 'Remote')}</div>
            <div class="score">Match: {job['score']}%</div>
            
            <div class="skills">
"""
        
        if present:
            for skill in present[:4]:
                html += f'<span class="tag">✅ {skill}</span>'
        
        if missing:
            for skill in missing[:3]:
                html += f'<span class="tag missing">❌ {skill}</span>'
        
        html += f"""
            </div>
            <a href="{job['url']}" class="apply-btn" target="_blank">Apply Now →</a>
        </div>
"""

html += """
        <div class="footer">
            <p>JobPilot AI - Autonomous Job Discovery</p>
            <p>Notifications sent to: +91 8126394481</p>
        </div>
    </div>
</body>
</html>
"""

# Save notification page
with open('frontend/notification.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Notification page created!")
print("📄 Saved to: frontend/notification.html")
print("🌐 Access at: http://127.0.0.1:8000/static/notification.html")
print()
print("💡 Now when you get WhatsApp 'Hello World', open:")
print("   http://127.0.0.1:8000/static/notification.html")
print("   to see detailed job information!")
