from wedding.mailer import Mailer


class SendReminderMixin:

    @staticmethod
    def _create_message(user):
        return f"""
        Hi {user['first_name']},
        <br><br>
        We're super excited to having you at our wedding.
        To make sure we can plan the perfect wedding, we'd like to know if you
        will be there. 
        <br><br>
        Head to www.kumpfeiffer.wedding to fill out your RSVP with your invite
        code from your invitation.
        <br><br>
        Your invite code is: <strong>{user['username']}</strong>
        <br><br>
        Thanks, we're looking forward to seeing you on
        <strong>21 June 2023</strong> at Fingask Castle!
        <br><br>
        Best,<br>
        Kristina & Leo"""

    def send_reminder(self, request, queryset):

        mailer = Mailer()
        subject = "Reminder: RSVP for Kristina's and Leo's wedding!"

        for receiver in queryset.values("first_name", "username", "email"):
            message = self._create_message(receiver)
            mailer.send_mail(receiver["email"], subject, message)

    send_reminder.short_description = "Send reminder e-mail"
