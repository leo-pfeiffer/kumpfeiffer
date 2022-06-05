import os
import smtplib
import ssl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Mailer:

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    password = os.environ.get("MAILER_PASSWORD")
    sender_email = os.environ.get("MAILER_SENDER")

    def send_mail(self, receiver_email, subject, message):
        message = Mail(
            from_email=self.sender_email,
            to_emails=receiver_email,
            subject=subject,
            html_content=message)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
