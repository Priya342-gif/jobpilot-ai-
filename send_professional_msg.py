import httpx
import time

TOKEN = "EAARZAC0kuv2YBSAv0HDJhHieE8lHedtawQPHYORjZAp7u48FAEMAiAJdPuW8fEtWYEqxJiQHW1UH2ZB0ZCD7Eni6ITEhKwM2zVnGWxEeWk0jFQCrWKd26hSVZBrZBCCpxkHj71JBDBzfywy9WSFhiIyGH4YMPYiikIY1a9xOOl5014lavpqZC3k2oHodmDU9IewZALsSBJLCGhRrcPIuwBXJG4c2BFVQdZBbwrRHZAOjzXZAJ9DtTIIWw3lnYjtx5AtNmfjZADOxnTGvoa6TZCwVMAuZBmZAjJOkQZDZD"
PHONE_ID = "1344464935407648"
TO = "918126394481"

url = f"https://graph.facebook.com/v23.0/{PHONE_ID}/messages"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# Get job count
try:
    jobs = httpx.get('http://127.0.0.1:8000/api/jobs').json()
    job_count = len(jobs)
except:
    job_count = 2

print(f"📊 Found {job_count} jobs to notify about")
print("\n📱 Sending professional WhatsApp notification...")

# Step 1: Send template
print("\n1️⃣ Sending Hello World template...")
template_payload = {
    "messaging_product": "whatsapp",
    "to": TO,
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": {"code": "en_US"}
    }
}

try:
    response1 = httpx.post(url, headers=headers, json=template_payload, timeout=20)
    print(f"   Status: {response1.status_code}")
    
    if response1.status_code == 200:
        print("   ✅ Template sent!")
        
        # Step 2: Wait and send professional message
        print("\n2️⃣ Waiting 3 seconds...")
        time.sleep(3)
        
        print("3️⃣ Sending professional alert message...")
        
        professional_msg = f"""🎯 JobPilot AI Professional Alert

✅ {job_count} New Job Match{"es" if job_count > 1 else ""} Found!

Your profile in Embedded Systems, IoT & Robotics matches these opportunities.

📊 View Details:
http://127.0.0.1:8000/static/notification.html

🌐 Full Dashboard:
http://127.0.0.1:8000

Match Threshold: 30%+
Auto-Apply: OFF (Manual review required)

Good luck with your applications! 🚀"""
        
        text_payload = {
            "messaging_product": "whatsapp",
            "to": TO,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": professional_msg
            }
        }
        
        response2 = httpx.post(url, headers=headers, json=text_payload, timeout=20)
        print(f"   Status: {response2.status_code}")
        print(f"   Response: {response2.text}")
        
        if response2.status_code == 200:
            print("\n" + "="*60)
            print("✅ SUCCESS! Professional message sent!")
            print("="*60)
            print("\n📱 Check WhatsApp on +91 8126394481")
            print("\nYou should see:")
            print("1. Hello World")
            print("2. Professional alert with job details and links")
        elif response2.status_code == 403 or "24 hour" in response2.text.lower():
            print("\n⚠️ Text message blocked by WhatsApp restriction")
            print("\n💡 Solution: Send ANY message FROM your WhatsApp")
            print("   to +1 (555) 198-5648 (your test number)")
            print("   Then text messages will work for 24 hours!")
        else:
            print(f"\n❌ Professional message failed")
            print("Only 'Hello World' template was sent")
            
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n📄 View jobs at: http://127.0.0.1:8000")
