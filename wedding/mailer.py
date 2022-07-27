import os
import requests


class Mailer:

    API_KEY = os.environ.get("MAILGUN_API_KEY")
    API_BASE_URL = os.environ.get("MAILGUN_API_URL")

    # todo BCC
    # todo reply to my personal email

    @classmethod
    def send_simple_message(cls):
        return requests.post(
            f"{cls.API_BASE_URL}/messages",
            auth=("api", cls.API_KEY),
            data={
                "from": "Kumpf-Pfeiffer Wedding <mailgun@kumpfeiffer.wedding>",
                "to": [
                    "leopold.pfeiffer@gmx.de",
                ],
                "subject": "Hello",
                "text": "Hello Babsy, with this we can automate our wedding emails!",
            },
        )

    @classmethod
    def send_mail(cls, receiver_email, subject, message):
        return requests.post(
            f"{cls.API_BASE_URL}/messages",
            auth=("api", cls.API_KEY),
            data={
                "from": "Kumpf-Pfeiffer Wedding <mailgun@kumpfeiffer.wedding>",
                "to": [receiver_email],
                "subject": subject,
                "text": message,
            },
        )


Mailer.send_simple_message()
