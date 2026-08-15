import httpx

TOKEN = "EAARZAC0kuv2YBSAv0HDJhHieE8lHedtawQPHYORjZAp7u48FAEMAiAJdPuW8fEtWYEqxJiQHW1UH2ZB0ZCD7Eni6ITEhKwM2zVnGWxEeWk0jFQCrWKd26hSVZBrZBCCpxkHj71JBDBzfywy9WSFhiIyGH4YMPYiikIY1a9xOOl5014lavpqZC3k2oHodmDU9IewZALsSBJLCGhRrcPIuwBXJG4c2BFVQdZBbwrRHZAOjzXZAJ9DtTIIWw3lnYjtx5AtNmfjZADOxnTGvoa6TZCwVMAuZBmZAjJOkQZDZD"
PHONE_ID = "1344464935407648"
TO = "918126394481"

print("📱 Sending WhatsApp with Hello World template...")
print()

# First send hello_world template
url = f"https://graph.facebook.com/v23.0/{PHONE_ID}/messages"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# Send template
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
    print(f"Template Status: {response1.status_code}")
    
    if response1.status_code == 200:
        print("✅ 'Hello World' template sent!")
        
        # Wait a moment then try to send a follow-up text with link
        import time
        time.sleep(2)
        
        print("\n📲 Now sending follow-up message with link...")
        
        # Try to send text message (this might work after template message)
        text_payload = {
            "messaging_product": "whatsapp",
            "to": TO,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": "🎯 JobPilot AI - View your job matches:\n\nhttp://127.0.0.1:8000/static/notification.html\n\nOr open full dashboard:\nhttp://127.0.0.1:8000"
            }
        }
        
        response2 = httpx.post(url, headers=headers, json=text_payload, timeout=20)
        print(f"Link Message Status: {response2.status_code}")
        print(f"Response: {response2.text}")
        
        if response2.status_code == 200:
            print("\n✅ SUCCESS! Link message sent!")
            print("📱 Check WhatsApp - you should see:")
            print("   1. 'Hello World' message")
            print("   2. Link to notification page")
        else:
            print("\n⚠️ Link message not sent (WhatsApp restriction)")
            print("💡 Solution: Message the business number first, then links will work!")
            
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("\n📄 ALWAYS AVAILABLE:")
print("   Notification Page: http://127.0.0.1:8000/static/notification.html")
print("   Full Dashboard: http://127.0.0.1:8000")
print("\n💡 Bookmark these links on your phone!")
