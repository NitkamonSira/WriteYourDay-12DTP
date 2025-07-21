import smtplib
from smtplib import SMTPRecipientsRefused, SMTPServerDisconnected

def send_email(sender_email, sender_email_password, reciever_email, message):
    session = None
    try:
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_email, sender_email_password)
        session.sendmail(sender_email, reciever_email, message)
        print(f"Email sent successfully to {reciever_email}!")
    except SMTPRecipientsRefused:
        print(f"Error: Recipient email refused.")
    except SMTPServerDisconnected:
        print(f"Error: SMTP server disconnected.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        session.quit()
    
with open('email_password.txt', 'r') as file:
    lines = file.readlines()
    sender_email = lines[0].strip()
    sender_email_password = lines[1].strip()
           