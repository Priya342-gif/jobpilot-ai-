import httpx

TOKEN = "EAARZAC0kuv2YBSNJxoiSaAtBKA4x1JGPUXWBEf92OxF59p9ZAdnJGtd4oS6rThbL7ZAtmLmem2NQLeZCeNU7L7KVodJ9AgLSt6sjTfoc4S0lAMIV0GflV8EfwxH87uUZBOZAkzFJZBaNuyDm2YWQIcvZB0RK2ZAWZAz31zLYzU9fN1ZC5XKQse2TZC13RN8ZCEUYrSaJfgWchK1XeeWNcaM31ZCCnhED6FKIepx4MUkRKTCAqMd9GaD6frwISB8AHZB9qZAZAvl6FcTv552B6UOUrBrUDfzr6mtKm"
PHONE_ID = "1344464935407648"

print("🔍 Verifying WhatsApp Business API Setup...\n")

# Test 1: Check if token is valid by getting account info
print("Test 1: Checking token validity...")
headers = {"Authorization": f"Bearer {TOKEN}"}

try:
    # Try to get business account info
    response = httpx.get(
        f"https://graph.facebook.com/v23.0/{PHONE_ID}",
        headers=headers,
        timeout=20
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}\n")
    
    if response.status_code == 200:
        print("✅ Token is valid!")
    else:
        print("❌ Token issue detected")
        print("\n💡 Possible reasons:")
        print("1. Token expired (they expire after 24 hours by default)")
        print("2. App needs 'whatsapp_business_messaging' permission")
        print("3. Phone number not verified")
        print("\n🔧 Fix:")
        print("Go to Meta Console → Your App → WhatsApp → Configuration")
        print("Make sure 'whatsapp_business_messaging' permission is granted")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("\n📱 Meanwhile, your jobs are available at:")
print("   http://127.0.0.1:8000")
print("\n💡 You can use Email notifications instead (more reliable)!")
