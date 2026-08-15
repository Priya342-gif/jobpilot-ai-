import smtplib
from email.message import EmailMessage
from backend.config import settings

def send_email(subject: str, body: str) -> bool:
    if not all([
        settings.smtp_host,
        settings.smtp_username,
        settings.smtp_password,
        settings.notify_email_to,
    ]):
        print("[JobPilot] Email not configured.")
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_username
    message["To"] = settings.notify_email_to
    message.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message)

    return True
