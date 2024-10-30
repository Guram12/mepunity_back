from django.db import models



class Project(models.Model):
    title_ka = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    description_ka = models.TextField(max_length=3000 )
    description_en = models.TextField(max_length=3000 )

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
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)
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
        return f"{self.name_ka} - {self.price_per_sqm} - {self.discount_percentage}%"












