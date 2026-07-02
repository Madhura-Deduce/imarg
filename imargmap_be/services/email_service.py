import os
import ssl
import smtplib
from pathlib import Path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "templates" / "verify_email.html"


def send_verification_email(
    email: str,
    full_name: str,
    token: str
):
    BACKEND_URL = os.getenv("BACKEND_URL")

    verification_link = (
        f"{BACKEND_URL}/auth/verify-email?token={token}"
    )

    print("\n==============================")
    print("Verification Email")
    print("Recipient :", email)
    print("Token     :", token)
    print("Link      :", verification_link)
    print("==============================\n")

    try:

        with open(
            TEMPLATE_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            html = file.read()

        html = html.replace(
            "{{full_name}}",
            full_name
        )

        html = html.replace(
            "{{verification_link}}",
            verification_link
        )

        message = MIMEMultipart("alternative")
        message["Subject"] = "Verify your email address"
        message["From"] = SMTP_USERNAME
        message["To"] = email

        message.attach(
            MIMEText(html, "html")
        )

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT,
            context=context,
            timeout=30
        ) as server:

            server.login(
                SMTP_USERNAME,
                SMTP_PASSWORD
            )

            server.sendmail(
                SMTP_USERNAME,
                email,
                message.as_string()
            )

        print("Verification email sent successfully.")

    except Exception as e:

        print("SMTP ERROR:", str(e))
        raise Exception(
            f"Email sending failed: {str(e)}"
        )