from django.db import models
from django.core.exceptions import ValidationError



class Project(models.Model):
    title_ka = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    description_ka = models.TextField(max_length=3000 )
    description_en = models.TextField(max_length=3000 )
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title_ka
    
    def delete(self, *args, **kwargs):
        # Delete related images from S3
        for image in self.images.all():
            image.image.delete(save=False)
        # Delete the project instance
        super().delete(*args, **kwargs)

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects')

    def __str__(self):
        return f"Image for {self.project.title_ka}"


# -------------------------------------------------------------------------------------------

class ProjectService(models.Model):
    name_ka = models.CharField(max_length=255, unique=True)
    name_en = models.CharField(max_length=255, unique=True)
    price_per_sqm_below_hotel = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_sqm_above_hotel = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_sqm_below_residential = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_sqm_above_residential = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_sqm_below_enterprise = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_sqm_above_enterprise = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    ELECTRICAL = 'electrical'
    MECHANICAL = 'mechanical'
    PLUMBING = 'plumbing'

    DTYPE_CHOICES = [
        (ELECTRICAL, 'Electrical'),
        (MECHANICAL, 'Mechanical'),
        (PLUMBING, 'Plumbing'),
    ]
    dtype = models.CharField(max_length=50, choices=DTYPE_CHOICES)


    def __str__(self):
        return f"{self.name_ka} - {self.price_per_sqm_below_hotel} - {self.price_per_sqm_above_hotel} - {self.discount_percentage}%"




class Minimum_Amount_Of_Space(models.Model):
    space = models.IntegerField()

    def __str__(self):
        return  f"{self.space} m2"

    def save(self, *args, **kwargs):
        if not self.pk and Minimum_Amount_Of_Space.objects.exists():
            raise ValidationError('There can be only one instance of Minimum_Amount_Of_Space')
        super().save(*args, **kwargs)






