from django.db import models


# const electricityProjectData: Project_Data_Types[] = [
#   { imgSrc: pdf_image, fileSize: "144 KB", downloadLink: "/test.pdf" },
#   { imgSrc: pdf_image, fileSize: "55 KB", downloadLink: "/test.pdf" },
#   { imgSrc: pdf_image, fileSize: "20 MB", downloadLink: "/test.pdf" },
#   { imgSrc: pdf_image, fileSize: "46 KB", downloadLink: "/test.pdf" },


# saxeli,
# proeqtis surati ,
# desqripotion 


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='projects')

    def __str__(self):
        return self.title
    









