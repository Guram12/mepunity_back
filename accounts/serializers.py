from rest_framework.serializers import ModelSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser





class AccountSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ "id", "email", "username", "company" ,"phone_number", "discount", "is_email_verified", "image"]
        read_only_fields = [ "id",'is_email_verified', 'discount']




class CustomRegisterSerializer(RegisterSerializer):
    company = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['company'] = self.validated_data.get('company', '')
        data['phone_number'] = self.validated_data.get('phone_number', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.company = self.cleaned_data.get('company')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        return user








