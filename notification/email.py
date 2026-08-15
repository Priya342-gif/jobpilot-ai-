import smtplib
from email.message import EmailMessage
from backend.config import settings
import os

def send_email(subject: str, body: str) -> bool:
    # Try SendGrid first (works on Render)
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    if sendgrid_api_key:
        try:
            import httpx
            response = httpx.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {sendgrid_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "personalizations": [{
                        "to": [{"email": settings.notify_email_to}]
                    }],
                    "from": {"email": settings.smtp_username, "name": "JobPilot AI"},
                    "subject": subject,
                    "content": [{"type": "text/plain", "value": body}]
                },
                timeout=10
            )
            response.raise_for_status()
            print("[JobPilot] Email sent via SendGrid!")
            return True
        except Exception as e:
            print(f"[JobPilot] SendGrid failed: {e}")
    
    # Fallback to SMTP (works locally, not on Render free tier)
    if not all([
        settings.smtp_host,
        settings.smtp_username,
        settings.smtp_password,
        settings.notify_email_to,
    ]):
        print("[JobPilot] Email not configured.")
        return False

    try:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = settings.smtp_username
        message["To"] = settings.notify_email_to
        message.set_content(body)

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
        
        print("[JobPilot] Email sent via SMTP!")
        return True
    except Exception as e:
        print(f"[JobPilot] SMTP failed: {e}")
        return False
