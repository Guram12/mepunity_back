from django.shortcuts import render
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.core.mail import EmailMessage
from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import logging




class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]








logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def send_file_to_email(request):
    parser_classes = (MultiPartParser, FormParser)
    file = request.FILES.get('file')
    name = request.data.get('name')
    company = request.data.get('company')
    email = request.data.get('email')
    subject = request.data.get('subject', 'No Subject')
    description = request.data.get('description', 'No Description')

    logger.debug(f"File: {file}, Name: {name}, Company: {company}, Email: {email}, Subject: {subject}, Description: {description}")

    if not name:
        return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
    if not company:
        return Response({'error': 'Company is required'}, status=status.HTTP_400_BAD_REQUEST)
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        email_message = EmailMessage(
            subject=f"File Upload: {subject}",
            body=f"Name: {name}\nCompany: {company}\nEmail: {email}\nDescription: {description}",
            from_email=email,
            to=['g.nishnianidze97@gmail.com'],
        )

        if file:
            email_message.attach(file.name, file.read(), file.content_type)
            logger.debug(f"Attached file: {file.name}")

        email_message.send()
        logger.info(f"Email sent: {email_message}")

        return Response({'message': 'File uploaded and email sent successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    






import boto3
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from botocore.exceptions import NoCredentialsError


@api_view(['POST'])
@permission_classes([AllowAny])
def send_file_to_email(request):
    parser_classes = (MultiPartParser, FormParser)
    file = request.FILES.get('file')
    name = request.data.get('name')
    company = request.data.get('company')
    email = request.data.get('email')
    subject = request.data.get('subject', 'No Subject')
    description = request.data.get('description', 'No Description')

    logger.debug(f"File: {file}, Name: {name}, Company: {company}, Email: {email}, Subject: {subject}, Description: {description}")

    if not name:
        return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
    if not company:
        return Response({'error': 'Company is required'}, status=status.HTTP_400_BAD_REQUEST)
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Upload file to AWS S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file.name)

        # Generate pre-signed URL
        file_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': file.name},
            ExpiresIn=3600  # URL expiration time in seconds
        )

        context = {
            'name': name,
            'company': company,
            'email': email,
            'subject': subject,
            'description': description,
            'file_url': file_url,
        }
        message = render_to_string('accounts/email_template.html', context)  # Ensure you have this template

        send_mail(
            subject=f"File Upload: {subject}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['g.nishnianidze97@gmail.com'],
        )

        logger.info("Email sent successfully.")
        return Response({'message': 'File uploaded and email sent successfully'}, status=status.HTTP_200_OK)
    except NoCredentialsError:
        logger.error("AWS credentials not available.")
        return Response({'error': 'AWS credentials not available'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)