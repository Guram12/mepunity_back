import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mepunity.settings')

import django
django.setup()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmationHMAC
from django.shortcuts import redirect
import logging
from .models import CustomUser , Discount
from django.conf import settings



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
            # Redirect to frontend login page with query parameter
            return redirect(f'{settings.FRONTEND_URL}?isAuthenticated=false')  
        else:
            logger.error("Confirmation not found, returning invalid template")
            return redirect(f'{settings.FRONTEND_URL}') 
        
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer , ProfileFinishSerializer , ProfileUpdateSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    




class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = AccountSerializer(user)
        return Response(serializer.data)
    


from rest_framework import status

class ProfileFinishView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ProfileFinishSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            errors = serializer.errors
            if 'username' in errors:
                errors['username'] = ['This username is already taken.']
            if 'company_name' in errors:
                errors['company_name'] = ['This company name is already taken.']
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# ===================================== custom login view =====================================


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# ========================================= profle update view =====================================



from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileUpdateSerializer

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# ===================================  password reset ===================================


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class PasswordResetRequestView(APIView):
    permission_classes = [] 

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
        
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        
        return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    permission_classes = []  
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password has been reset'}, status=status.HTTP_200_OK)



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

        if created:
            # Create a Discount instance with default value 0
            Discount.objects.create(user=user)

        if not created:
            user.is_email_verified = True
            user.save()

        return user

    def generate_unique_username(self, base_username):
        while True:
            username = f"{base_username}_{get_random_string(5)}"
            if not CustomUser.objects.filter(username=username).exists():
                return username
            

