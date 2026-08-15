import httpx
from backend.config import settings

# Get current jobs from API
jobs = httpx.get('http://127.0.0.1:8000/api/jobs').json()

print(f"Found {len(jobs)} jobs in database")

if jobs:
    # Get top 3 matches
    top_jobs = jobs[:3]
    
    print("\nSending WhatsApp notification for top jobs...")
    
    # Send template notification
    url = f"https://graph.facebook.com/v23.0/{settings.whatsapp_phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json",
    }
    
    # Use hello_world template (only one available)
    payload = {
        "messaging_product": "whatsapp",
        "to": settings.whatsapp_to,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {"code": "en_US"}
        }
    }
    
    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=20)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ WhatsApp notification sent!")
            print(f"📱 Check WhatsApp on +91 8126394481")
            print(f"\nNotification is for these jobs:")
            for i, job in enumerate(top_jobs, 1):
                print(f"{i}. {job['title']} at {job['company']} - {job['score']}% match")
            print(f"\n🌐 View all jobs: http://127.0.0.1:8000")
        else:
            print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("No jobs found yet. Worker will find jobs automatically every 20 minutes.")
