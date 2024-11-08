from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
import os
import boto3
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False) 
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    company = models.CharField(max_length=255, blank=True, null=True , unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


    def save(self, *args, **kwargs):
        try:
            old_instance = CustomUser.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                s3 = boto3.resource('s3')
                try:
                    s3.Object(settings.AWS_STORAGE_BUCKET_NAME, f"media/{old_instance.image.name}").delete()
                    logger.info(f"Deleted old image: media/{old_instance.image.name}")
                except Exception as e:
                    logger.error(f"Error deleting old image: {e}")
        except CustomUser.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def delete_profile_picture(self):
        if self.image:
            s3 = boto3.resource('s3')
            try:
                s3.Object(settings.AWS_STORAGE_BUCKET_NAME, f"media/{self.image.name}").delete()
                self.image = None
                self.save()
                logger.info(f"Deleted profile picture: media/{self.image.name}")
            except Exception as e:
                logger.error(f"Error deleting profile picture: {e}")


from django.db import models
from django.conf import settings

class Discount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discount = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.user.email} - {self.discount}%"