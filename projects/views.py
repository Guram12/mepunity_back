from .models import Project , Minimum_Amount_Of_Space
from .serializers import ProjectSerializer, MinimumSpaceSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.http import JsonResponse
from rest_framework.decorators import api_view , permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-priority') 
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]




class MinimumSpaceViewSet(viewsets.ModelViewSet):
    queryset = Minimum_Amount_Of_Space.objects.all()
    serializer_class = MinimumSpaceSerializer
    permission_classes = [AllowAny]



import cloudinary.uploader

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def send_file_to_email(request):

    files = request.FILES.getlist('files')

    name = request.data.get('name')
    company = request.data.get('company')
    email = request.data.get('email')

    subject = request.data.get('subject', 'No Subject')
    description = request.data.get('description', 'No Description')

    if not name or not company or not email:
        return Response(
            {'error': 'Name, Company, and Email are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:

        file_urls = []

        for file in files:

            result = cloudinary.uploader.upload(
                file,
                folder=f"uploaded_data_sent_email/{company}",
                resource_type="auto",
                use_filename=True,
                unique_filename=True,
                overwrite=False,
            )

            file_urls.append({
                'file_name': file.name,
                'file_url': result['secure_url']
            })

        context = {
            'name': name,
            'company': company,
            'email': email,
            'subject': subject,
            'description': description,
            'file_urls': file_urls,
        }

        message = render_to_string(
            'accounts/email_template.html',
            context
        )

        send_mail(
            subject=f"File Upload: {subject}",
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['g.nishnianidze97@gmail.com'],
            html_message=message,
            fail_silently=False,
        )

        return Response(
            {'message': 'Files uploaded and email sent successfully'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {'error': f'Failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
# ==========================================  project price view  ==========================================


from django.http import JsonResponse
from .models import ProjectService
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([AllowAny])
def project_services_list(request):
    services = ProjectService.objects.all()
    data = [
        {   
            'id': service.id,
            "dtype" : service.dtype,
            'name_ka': service.name_ka,
            'name_en': service.name_en,
            'price_per_sqm_below_hotel': service.price_per_sqm_below_hotel,
            'price_per_sqm_above_hotel': service.price_per_sqm_above_hotel,

            'price_per_sqm_below_residential': service.price_per_sqm_below_residential,
            'price_per_sqm_above_residential': service.price_per_sqm_above_residential,

            'price_per_sqm_below_enterprise': service.price_per_sqm_below_enterprise,
            'price_per_sqm_above_enterprise': service.price_per_sqm_above_enterprise,


            'discount_percentage': service.discount_percentage,
        }
        for service in services
    ]
    return JsonResponse(data, safe=False)

