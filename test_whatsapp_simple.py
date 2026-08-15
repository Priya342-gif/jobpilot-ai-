from notification.whatsapp import send_whatsapp

try:
    success = send_whatsapp("🧪 Test from JobPilot AI - If you see this, WhatsApp is working!")
    if success:
        print("✅ WhatsApp message sent successfully!")
        print("Check your WhatsApp: +919795675534")
    else:
        print("❌ WhatsApp not configured or failed")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n⚠️ Your WhatsApp token is expired or invalid.")
    print("Get a new token from: https://developers.facebook.com/")
