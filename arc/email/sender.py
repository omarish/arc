import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# Email settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "omar.bohsali@gmail.com"


def send_email(to: str, subject: str, attachment: str, app_password: str) -> None:
    """Send an email with an attachment using Gmail SMTP."""
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to
    msg["Subject"] = subject

    # Attach file
    part = MIMEBase("application", "octet-stream")
    with open(attachment, "rb") as f:
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
    msg.attach(part)

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, app_password)
        server.send_message(msg)
