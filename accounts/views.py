from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmationHMAC
from django.shortcuts import redirect
import logging
from . models import CustomUser

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
            return redirect('http://localhost:5173')  # Redirect to frontend login page
        else:
            logger.error("Confirmation not found, returning invalid template")
            return redirect('http://localhost:5173/') 
        


from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer , ProfileUpdateSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = AccountSerializer(user)
        return Response(serializer.data)
    


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        




# =================================== Google Login view  =================================== 

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
import requests



logger = logging.getLogger(__name__)

class CustomGoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        response = super().get_response()
        user = self.user
        if SocialAccount.objects.filter(user=user, provider='google').exists():
            user.is_email_verified = True
            user.save()
        return response

    def post(self, request, *args, **kwargs):
        logger.debug(f"Request data: {request.data}")
        id_token = request.data.get('id_token')
        if not id_token:
            return Response({'error': 'id_token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the id_token with Google
        try:
            response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
            response_data = response.json()
            if 'error_description' in response_data:
                raise OAuth2Error(response_data['error_description'])
        except OAuth2Error as e:
            logger.error(f"Error verifying id_token: {e}")
            return Response({'error': 'Invalid id_token'}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get the user
        try:
            user = self.get_user_from_response(response_data)
            self.user = user

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access': access_token,
                'refresh': refresh_token,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error during user creation: {e}")
            return Response({'error': 'Error during user creation'}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_from_response(self, response_data):
        email = response_data['email']
        base_username = email.split('@')[0]
        username = base_username

        # Check if the username already exists and generate a unique one if necessary
        if CustomUser.objects.filter(username=username).exists():
            username = self.generate_unique_username(base_username)

        user, created = CustomUser.objects.get_or_create(email=email, defaults={
            'username': username,
            'is_email_verified': True,
        })

        if not created:
            user.is_email_verified = True
            user.save()

        return user

    def generate_unique_username(self, base_username):
        while True:
            username = f"{base_username}_{get_random_string(5)}"
            if not CustomUser.objects.filter(username=username).exists():
                return username
            
# =========================================================================================================







