from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False) 
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    company = models.CharField(max_length=255, blank=True, null=True , unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

from django.db import models
from django.conf import settings

class Discount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discount = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.user.email} - {self.discount}%"