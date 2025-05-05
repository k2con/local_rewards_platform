import os

from core.settings import *


DEBUG = bool(os.environ.get('DEBUG', False))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('RDS_DB_NAME'),
        'USER': os.environ.get('RDS_USERNAME'),
        'PASSWORD': os.environ.get('RDS_PASSWORD'),
        'HOST': os.environ.get('RDS_HOSTNAME'),
        'PORT': os.environ.get('RDS_PORT')
    }
}


ALLOWED_HOSTS = [
    'megadash.masamo.tech',
    'megadash-stg.masamo.tech',
]
