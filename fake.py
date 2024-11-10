import os
import random
from faker import Faker
from django.core.files import File
from django.core.exceptions import ImproperlyConfigured

# Ensure settings are configured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mepunity.settings')

import django
django.setup()

from projects.models import Project, ProjectImage  # Adjust the import according to your app name

# Initialize Faker
fake = Faker()

# Directory containing images
image_dir = 'images'

# List of image file paths
image_files = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, img))]

# Function to create fake Project instances
def create_fake_projects(n):
    for _ in range(n):
        project = Project(
            title_ka=fake.sentence(nb_words=3),
            title_en=fake.sentence(nb_words=3),
            description_ka=fake.text(max_nb_chars=3000),
            description_en=fake.text(max_nb_chars=3000)
        )
        project.save()

        number_images = random.randint(1, 5)
        # Add exactly 3 images to the project
        selected_images = random.sample(image_files, number_images)
        for image_path in selected_images:
            with open(image_path, 'rb') as img_file:
                project_image = ProjectImage(
                    project=project,
                    image=File(img_file, name=os.path.basename(image_path))
                )
                project_image.save()

create_fake_projects(50)