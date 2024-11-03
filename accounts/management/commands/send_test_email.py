from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **kwargs):
        context = {
            'user': {'username': 'testuser'},
            'activate_url': 'http://example.com/activate'
        }
        subject = 'Test Email'
        message = render_to_string('accounts/email_confirmation_message.html', context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['g.nishnianidze97@gmail.com'])
        self.stdout.write(self.style.SUCCESS('Test email sent successfully'))