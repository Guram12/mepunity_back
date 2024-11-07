from rest_framework.serializers import ModelSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser, Discount

class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Discount
        fields = ['discount']

class AccountSerializer(ModelSerializer):
    discount = serializers.IntegerField(source='discount.discount', read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "company", "phone_number", "discount", "is_email_verified", "image"]
        read_only_fields = ["id", 'is_email_verified', "discount"]

class ProfileFinishSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'company', 'phone_number']


# ============================= profile update  serializer =====================================


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'is_email_verified', 'image', 'company', 'first_name', 'last_name', 'username']




# =================================== Custom login serializer ====================================
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_email_verified:
            print(f"User {user.email} tried to log in without verifying email.")
            raise ValidationError({'email': 'Email is not verified. Please check your email to verify your account.'})

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
# ============================= Custom Register Serializer ==============================

from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

class CustomRegisterSerializer(RegisterSerializer):
    company = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['company'] = self.validated_data.get('company', '')
        data['phone_number'] = self.validated_data.get('phone_number', '')
        return data

    def save(self, request):
        try:
            user = super().save(request)
            user.company = self.cleaned_data.get('company')
            user.phone_number = self.cleaned_data.get('phone_number')
            user.save()

            Discount.objects.create(user=user, discount=0)

            return user
        except IntegrityError as e:
            if 'accounts_customuser_email_key' in str(e):
                raise ValidationError({'email': 'Email already exists'})
            raise ValidationError({'detail': 'An error occurred during registration'})