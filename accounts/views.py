from django.shortcuts import render
import logging
from allauth.account.views import ConfirmEmailView
from django.shortcuts import redirect
from allauth.account.models import EmailConfirmationHMAC


logger = logging.getLogger(__name__)

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, request, *args, **kwargs):
        logger.info("Entering CustomConfirmEmailView")
        confirmation = EmailConfirmationHMAC.from_key(kwargs['key'])
        if confirmation:
            logger.info("Confirmation found, confirming...")
            confirmation.confirm(request)
            user = confirmation.email_address.user
            user.is_email_verified = True  
            user.save()
            return redirect('http://localhost:5174/login')  # Redirect to frontend login page
        else:
            logger.error("Confirmation not found, returning invalid template")
            return redirect('http://localhost:5174/login') 
        

