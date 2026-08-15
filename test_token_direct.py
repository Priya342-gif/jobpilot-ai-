import httpx

# Use the exact token from your message
TOKEN = "EAARZAC0kuv2YBSNJxoiSaAtBKA4x1JGPUXWBEf92OxF59p9ZAdnJGtd4oS6rThbL7ZAtmLmem2NQLeZCeNU7L7KVodJ9AgLSt6sjTfoc4S0lAMIV0GflV8EfwxH87uUZBOZAkzFJZBaNuyDm2YWQIcvZB0RK2ZAWZAz31zLYzU9fN1ZC5XKQse2TZC13RN8ZCEUYrSaJfgWchK1XeeWNcaM31ZCCnhED6FKIepx4MUkRKTCAqMd9GaD6frwISB8AHZB9qZAZAvl6FcTv552B6UOUrBrUDfzr6mtKm"
PHONE_ID = "1344464935407648"
TO = "918126394481"

url = f"https://graph.facebook.com/v23.0/{PHONE_ID}/messages"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

payload = {
    "messaging_product": "whatsapp",
    "to": TO,
    "type": "template",
    "template": {
        "name": "hello_world",
        "language": {"code": "en_US"}
    }
}

print(f"Sending to: {TO}")
print(f"Token length: {len(TOKEN)}")
print()

try:
    response = httpx.post(url, headers=headers, json=payload, timeout=20)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ WhatsApp message sent!")
        print("📱 Check WhatsApp on +91 8126394481")
    else:
        print("\n❌ Failed - Token may be invalid")
        print("Please generate a new token from Meta console")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
