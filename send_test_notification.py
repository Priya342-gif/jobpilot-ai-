from notification.whatsapp import send_whatsapp

message = """🎉 JobPilot AI - WhatsApp Connected!

✅ Your number: +91 8126394481
✅ Notifications are ACTIVE

You will receive job alerts when:
- Match score ≥ 30%
- New jobs found every 20 minutes

Dashboard: http://127.0.0.1:8000

JobPilot AI is working! 🚀"""

try:
    success = send_whatsapp(message)
    if success:
        print("✅ WhatsApp notification sent to +91 8126394481!")
        print("📱 Check your WhatsApp now!")
    else:
        print("❌ Failed to send")
except Exception as e:
    print(f"❌ Error: {e}")
