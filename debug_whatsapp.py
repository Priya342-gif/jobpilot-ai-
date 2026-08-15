import httpx
from backend.config import settings

print("=== WhatsApp Configuration ===")
print(f"Token: {settings.whatsapp_access_token[:50]}...")
print(f"Phone Number ID: {settings.whatsapp_phone_number_id}")
print(f"To: {settings.whatsapp_to}")
print()

url = (
    f"https://graph.facebook.com/v23.0/"
    f"{settings.whatsapp_phone_number_id}/messages"
)

headers = {
    "Authorization": f"Bearer {settings.whatsapp_access_token}",
    "Content-Type": "application/json",
}

payload = {
    "messaging_product": "whatsapp",
    "to": settings.whatsapp_to,
    "type": "text",
    "text": {"body": "Test from JobPilot AI - +91 8126394481"},
}

print(f"Sending to: {settings.whatsapp_to}")
print(f"URL: {url}")
print()

try:
    response = httpx.post(url, headers=headers, json=payload, timeout=20)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ Message sent successfully!")
        print("Check WhatsApp on +91 8126394481")
    else:
        print("\n❌ Failed to send")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
