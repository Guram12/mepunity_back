from rest_framework.serializers import ModelSerializer
from .models import CustomUser




class AccountSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ "id", "email", "username", "compamy" ,"phone_number", "discount", "is_email_verified", "image"]
        read_only_fields = [ "id",'is_email_verified', 'discount']









        