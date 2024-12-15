import boto3
from django.conf import settings
import os


session = boto3.Session(
    aws_access_key_id='AKIATX3PICNAR3JGAM55',
    aws_secret_access_key='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',
    region_name='eu-central-1'
)

s3 = session.resource('s3')
bucket = s3.Bucket('mep-unity-bucket')


# for obj in bucket.objects.all():
#     print(obj.key)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mepunity.settings')

print(settings.FRONTEND_URL)

