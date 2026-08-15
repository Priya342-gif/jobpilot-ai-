import httpx
from backend.config import settings

def send_whatsapp(text: str) -> bool:
    if not all([
        settings.whatsapp_access_token,
        settings.whatsapp_phone_number_id,
        settings.whatsapp_to,
    ]):
        print("[JobPilot] WhatsApp not configured.")
        return False

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{settings.whatsapp_phone_number_id}/messages"
    )

    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json",
    }

    # Try sending text message first
    payload = {
        "messaging_product": "whatsapp",
        "to": settings.whatsapp_to,
        "type": "text",
        "text": {"body": text},
    }

    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        return True
    except Exception as e:
        # If text fails, try template message
        print(f"[JobPilot] Text message failed: {e}")
        print("[JobPilot] Trying template message...")
        
        template_payload = {
            "messaging_product": "whatsapp",
            "to": settings.whatsapp_to,
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {"code": "en_US"}
            }
        }
        
        response = httpx.post(url, headers=headers, json=template_payload, timeout=20)
        response.raise_for_status()
        print("[JobPilot] Template message sent successfully!")
        return True
