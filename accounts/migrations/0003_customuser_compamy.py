# Generated by Django 5.1.2 on 2024-10-17 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='compamy',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
