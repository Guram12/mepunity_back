from rest_framework.serializers import ModelSerializer
from .models import CustomUser




class AccountSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['is_email_verified', 'discount']