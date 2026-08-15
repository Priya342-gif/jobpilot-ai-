import httpx
from backend.config import settings

# Try sending a template message (like Meta console does)
url = (
    f"https://graph.facebook.com/v23.0/"
    f"{settings.whatsapp_phone_number_id}/messages"
)

headers = {
    "Authorization": f"Bearer {settings.whatsapp_access_token}",
    "Content-Type": "application/json",
}

# First, let's see what templates are available
templates_url = f"https://graph.facebook.com/v23.0/{settings.whatsapp_phone_number_id}/message_templates"

try:
    print("Fetching available templates...")
    resp = httpx.get(templates_url, headers=headers, timeout=20)
    print(f"Templates Response: {resp.status_code}")
    print(resp.text)
    print()
except Exception as e:
    print(f"Error getting templates: {e}")
    print()

# Try sending with template (hello_world is default template)
payload = {
    "messaging_product": "whatsapp",
    "to": settings.whatsapp_to,
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": {
            "code": "en_US"
        }
    }
}

print(f"Sending template message to: {settings.whatsapp_to}")
print()

try:
    response = httpx.post(url, headers=headers, json=payload, timeout=20)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ Template message sent!")
        print("Check WhatsApp on +91 8126394481")
    else:
        print("\n❌ Failed to send template")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
