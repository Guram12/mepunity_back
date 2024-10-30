from .models import Project, ProjectImage, Minimum_Amount_Of_Space
from rest_framework import serializers

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class MinimumSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Minimum_Amount_Of_Space
        fields = '__all__'