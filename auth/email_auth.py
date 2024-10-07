"""For Email Auth"""
import smtplib
import logging
from email.mime.text import MIMEText

class EmailError(Exception):
    """Email Error"""

def send_auth_code(to_email: str, auth_code: str):
    """Email authentication

    Args:
        to_email (str): The target email
        auth_code (str): The 6-digit auth code
    """
    logger = logging.getLogger('auth')
    subject = f"Your Authentication Code is {auth_code}"
    body = f"Your authentication code is {auth_code}. Do not send this code to anyone.\
      If you did not request this code, do not take any action."

    # Email setup
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    # Sending email via SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        logger.info("Authentication code sent to %s", to_email)
    except EmailError as e:
        logger.error("Failed to send email: %s", e)
