import os
import environ
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab
from kombu import Exchange, Queue

# finding a root directory of the project
root = environ.Path(__file__) - 2

# setting roots for static, media, templates
templates_root = root('templates')

env = environ.Env()
# reading env file
environ.Env.read_env(env_file=root('.env'))
# site root points to rentAccess root folder
SITE_ROOT = root()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env.str('SECRET_KEY')
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

CORS_ORIGIN_ALLOW_ALL = env.bool('CORS_ORIGIN_ALLOW_ALL', default=True)

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
	'django.contrib.staticfiles',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'django.forms',
	'watchman',
	'django_extensions',
	'axes',
	'crispy_forms',
	'django_filters',
	'widget_tweaks',
	'django_countries',
	'storages',
	'tinymce',
	'timezone_field',
	'corsheaders',
	####################
	'userAccount',
	'mainPage',

]

SETTINGS_PATH = os.path.normpath(os.path.dirname(__file__))
CRISPY_TEMPLATE_PACK = 'bootstrap4'
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

SITE_ID = 1
MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'axes.middleware.AxesMiddleware',

]
AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesBackend',
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_USER_MODEL = 'userAccount.InternalUser'

ROOT_URLCONF = 'bcsproject.urls'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bcsproject.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# Databases
USE_POSTGRES = env.bool("USE_POSTGRES", False)
if USE_POSTGRES:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': env("DB_NAME"),
			"USER": env("DB_USER"),
			"PASSWORD": env("DB_PASSWORD"),
			"HOST": env("DB_HOST"),
			"PORT": env("DB_PORT"),
			"OPTIONS": {
				'options': '-c search_path=public'
			}
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': 'db.sqlite3',
		}
	}
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

################################################
# when DEBUG == True DRF will render errors as html pages
USE_S3 = env.bool('USE_S3', default=False)
if USE_S3:
	AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
	AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
	AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
	AWS_DEFAULT_ACL = 'public-read'
	AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
	AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
	# s3 static settings
	AWS_LOCATION = 'static'
	STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
	STATICFILES_STORAGE = 'bcsproject.storage_backends.StaticStorage'
	AWS_S3_REGION_NAME = "eu-north-1"
	AWS_S3_SIGNATURE_VERSION = "s3v4"
	# s3 public media settings
	PUBLIC_MEDIA_LOCATION = 'media'
	MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
	DEFAULT_FILE_STORAGE = 'bcsproject.storage_backends.PublicMediaStorage'
	# s3 private media settings
	PRIVATE_MEDIA_LOCATION = 'private'
	PRIVATE_FILE_STORAGE = 'bcsproject.storage_backends.PrivateMediaStorage'

else:
	STATIC_URL = '/static/'
	STATIC_ROOT = '/static/'
	MEDIA_ROOT = os.path.join('media')
	MEDIA_URL = '/media/'

# Static root and file definitions
STATICFILES_DIRS = [
	root("static"),
]

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default='redis://127.0.0.1:6379')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='redis://127.0.0.1:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'

default_exchange = Exchange('bcsproject_def', type='direct')
priority_exchange = Exchange('priority_queue', type='direct')

CELERY_QUEUES = (
	Queue('bcsproject_def', default_exchange, routing_key='bcsproject_def', consumer_arguments={'x-priority': 0}),
	Queue('priority_queue', priority_exchange, routing_key='priority_queue', consumer_arguments={'x-priority': 10}),
 )
CELERY_ROUTES = ({'bcsproject.tasks.send_submissions': {
						'queue': 'bcsproject_def',
						'routing_key': 'bcsproject_def'
				}}, )
CELERY_DEFAULT_QUEUE = 'bcsproject_def'
CELERY_DEFAULT_EXCHANGE = 'bcsproject_def'
CELERY_DEFAULT_ROUTING_KEY = 'bcsproject_def'
# AXES CONFIG
AXES_FAILURE_LIMIT = 7
AXES_LOCK_OUT_AT_FAILURE = True
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_RESET_ON_SUCCESS = True
AXES_COOLOFF_TIME = 24
AXES_META_PRECEDENCE_ORDER = [
   'HTTP_X_FORWARDED_FOR',
]
WATCHMAN_AUTH_DECORATOR = 'django.contrib.admin.views.decorators.staff_member_required'
