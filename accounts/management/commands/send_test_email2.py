from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **kwargs):
        subject = 'Test Email'
        message = 'This is a test email.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['g.nishnianidze97@gmail.com']

        try:
            send_mail(subject, message, from_email, recipient_list)
            self.stdout.write(self.style.SUCCESS('Test email sent successfully'))
            logger.info('Test email sent successfully')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send test email: {str(e)}'))
            logger.error(f'Failed to send test email: {str(e)}')