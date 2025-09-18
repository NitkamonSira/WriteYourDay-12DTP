import smtplib
import random

SERVER = "smtp.gmail.com"
PORT = 587
SENDER_EMAIL = "noreply.writeyourday@gmail.com"


def send_email(password, receiver_email, code, username):
    """Sends a verification email with a verification code.

    Args:
        password (str): The app password for the sender's email account.
        receiver_email (str): The recipient's email address.
        code (str): The verification code to include in the email.
        username (str): The name of the user to personalise the message.

    Returns:
        None
    """
    message = f"""\
Subject: Verification code

Hello {username},

Your verification code is:

{code}

Please enter this code to complete your verification process.

If you didn't request this code, please ignore this email.
Do not share this code with anyone.

Best regards,

Write Your Day"""
    try:
        with smtplib.SMTP(SERVER, PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, password)
            server.sendmail(SENDER_EMAIL, receiver_email, message)
            print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


def verification_code(num):
    """_summary_

    Args:
        num (int): length of the verification code

    Returns:
        str: num digits of verification code
    """
    number = ""
    for _ in range(num):
        code = random.randint(0, 9)
        number += str(code)
    return number
