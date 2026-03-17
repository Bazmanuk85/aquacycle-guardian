import smtplib
from email.mime.text import MIMEText


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"


def send_verification_email(email, token):

    link = f"https://yourdomain.com/verify/{token}"

    msg = MIMEText(
        f"Verify your AquaGuardian account:\n\n{link}"
    )

    msg["Subject"] = "Verify your AquaGuardian Account"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    server.starttls()

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    server.send_message(msg)

    server.quit()
