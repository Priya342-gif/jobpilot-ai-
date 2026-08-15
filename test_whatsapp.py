from notification.whatsapp import send_whatsapp

success = send_whatsapp(
    """🚀 JobPilot AI Test

WhatsApp integration is working!

The autonomous job monitor is ready to be connected.

Auto-apply: OFF
"""
)

print("Success:", success)