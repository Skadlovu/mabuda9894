from pathlib import Path
import os
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY =config('SECRET_KEY')



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD =config('EMAIL_HOST_PASSWORD')




DEBUG = True


ALLOWED_HOSTS = []


LOGIN_URL= 'login'


LOGIN_REDIRECT_URL= '/'

LOGOUT_REDIRECT_URL= '/'




CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"



CRISPY_TEMPLATE_PACK = 'bootstrap4'



DEFAULT_AUTO_FIELD= 'django.db.models.BigAutoField'





# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photos',
    'videos',
    'profiles',
    'crispy_forms',
    'crispy_bootstrap4',
    'watchanalytics',
    'payfast',
    #'stream',
    'django_q',
    'donations',
    'taggit',
    "corsheaders",
]

Q_CLUSTER = {
    'name': 'xxxworld',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,  # Set the timeout to a value suitable for your task
    'retry': 600,   # Set the retry to a value larger than the timeout
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
    'db_failures': 1000,
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'password': 'your_password',
        'socket_timeout': 3,
        'socket_connect_timeout': 3,
        'max_connections': 20,
        'retry_on_timeout': True,
        'skip_full': True
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xxxworld.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR ,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'xxxworld.wsgi.application'


ASGI_APPLICATION = 'stream.routing.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config('TIME_ZONE')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATICFILES_DIRS= [BASE_DIR /'static']

MEDIA_URL = '/media/'



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




#payfast
def payfast_url():
    from django.contrib.sites.models import Site
    site=Site.objects.get_current()
    return 'http: //{}'.format(site.domain)



PAYFAST_MERCHANT_ID=config('merchant_id')
PAYFAST_MERCHANT_KEY=config('merchant_key')
PAYFAST_URL_BASE= payfast_url


#Taggit
TAGGIT_CASE_INSENSITIVE=True


















"""""

AWS_ACCESS_KEY_ID='AKIAY45EECJPTWOIUVFZ'
AWS_SECRET_ACCESS_KEY_ID='qa1jRshq1wxz3XqiYVDp8U01Wzp2tQ72pw3WwEQ6'
AWS_STORAGE_BUCKET_NAME='xxxwfiles'
AWS_S3_REGION_NAME='eu-central-1'
AWS_DEFAULT_ACL= None
AWS_S3_OBJECTS_PARAMERTERS={'CacheControl':'max-age=86500'}
AWS_S3_CUSTOM_DOMAIN=f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com' 


STATIC_LOCATION='static'
STATIC_URL= f'{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE= 'xxxworld.storage_backends.StaticStorage'


PUBLIC_MEDIA_LOCATION='media'
MEDIA_URL= f'{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_STORAGE= 'xxxworld.storage_backends.PiblicMediaStorage'




#AWS_S3_SIGNATURE_NAME='s3v4'









#AWS Account settings
AWS_ACCESS_KEY_ID=config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY_ID=config('AWS_SECRET_ACCESS_KEY_ID')
AWS_STORAGE_BUCKET_NAME=config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME='eu-central-1'
AWS_DEFAULT_ACL= None
AWS_S3_OBJECTS_PARAMERTERS={'CacheControl':'max-age=86500'}
AWS_S3_CUSTOM_DOMAIN=f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'




#File location
STATIC_LOCATION='static'
STATIC_URL= f'{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

PUBLIC_MEDIA_LOCATION='media'
MEDIA_URL= f'{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'

#File storages
STORAGES = {
    # Media file (image) management
    "default": {
        "BACKEND": 'mysite.storage_backends.PiblicMediaStorage',
    },
    # CSS and JS file management
    "staticfiles": {
        "BACKEND": 'mysite.storage_backends.StaticStorage',
    },
}


#File storages

STATICFILES_STORAGE= 'mysite.storage_backends.StaticStorage'
DEFAULT_STORAGE= 'mysite.storage_backends.PiblicMediaStorage'

STORAGES = {
    # Media file (image) management
    "default": {
        "BACKEND": 'mysite.storage_backends.PiblicMediaStorage',
    },
    # CSS and JS file management
    "staticfiles": {
        "BACKEND": 'mysite.storage_backends.StaticStorage',
    },
}


"""





