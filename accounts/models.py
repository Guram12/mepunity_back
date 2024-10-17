from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    discount = models.IntegerField(default=0)
    is_email_verified = models.BooleanField(default=False) 
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    compamy = models.CharField(max_length=255, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
