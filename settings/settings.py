"""
Django settings for settings project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tuo6tg#zy)tnbjnpz3l2$51rln)tx2yh^4z41dvo(ifz)#ohtn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]

DATA_UPLOAD_MAX_NUMBER_FIELDS = None

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_crontab',
    "corsheaders",
    'graphene_django',
    
    
    'coreApp',
    'competitionApp',
    'teamApp',
    'fixtureApp',
    'statsApp',
    'bettingApp',
    'predictionApp',
]

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

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates/"],
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

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    
    'default': {
        'ENGINE'    : 'django.db.backends.mysql',
        'HOST'      : os.getenv("DB_HOST", "0.0.0.0"),
        'PORT'      : os.getenv("DB_PORT", 3306),
        'USER'      : os.getenv("DB_USER", "root"),
        'PASSWORD'  : os.getenv("DB_PASSWORD", "12345678"),
        'NAME'      : os.getenv("DB_NAME", "wikibet"),
    },
    
    
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# CRONJOBS
CRONTAB_DJANGO_PROJECT_NAME = "wikibet_crons"
CRONJOBS = [
    # ('*/3 * * * *', 'extra.new_fixtures.function', '>> {}'.format(os.path.join(BASE_DIR, "extra/logs/fixtures_job.log" ))),
    ('*/10 * * * *', 'coreApp.management.crons.new_fixtures.function', '>> {}'.format(os.path.join(BASE_DIR, "logs/fixtures_job.log" ))),
    ('*/10 * * * *', 'coreApp.management.crons.update_results.function', '>> {}'.format(os.path.join(BASE_DIR, "logs/results_job.log" ))),
    
    ('*/5 * * * *', 'coreApp.management.crons.facts.handle', '>> {}'.format(os.path.join(BASE_DIR, "logs/facts.log" ))),
    ('*/6 * * * *', 'coreApp.management.crons.before_stats_match.handle', '>> {}'.format(os.path.join(BASE_DIR, "logs/before_stats_match.log"))),
    ('*/7 * * * *', 'coreApp.management.crons.before_stats_match.handle2', '>> {}'.format(os.path.join(BASE_DIR, "logs/compared_elo.log"))),
    ('*/5 * * * *', 'coreApp.management.crons.team_profile.handle', '>> {}'.format(os.path.join(BASE_DIR, "logs/team_profile.log"))),
    ('*/15 * * * *', 'coreApp.management.crons.schedule_competition.handle', '>> {}'.format(os.path.join(BASE_DIR, "logs/schedule_competition.log" ))),
    
    ('0 */1 * * *', 'coreApp.management.crons.ranking.handle', '>> {}'.format(os.path.join(BASE_DIR, "logs/ranking.log" ))),
    
]


GRAPHENE = {
    "SCHEMA": "settings.schemas.schema",
    'SCHEMA_INDENT': 4,
    'MIDDLEWARE': [
        'graphene_django_extras.ExtraGraphQLDirectiveMiddleware'
    ]
}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
