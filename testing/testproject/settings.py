from __future__ import unicode_literals
import django

DEBUG = True
TEMPLATE_DEBUG = True

ROOT_URLCONF = 'testing.testproject.urls'

SECRET_KEY = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'testing.testproject',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

if not django.VERSION[:2] < (1, 7):
    INSTALLED_APPS += ('anylink.apps.AnyLinkConfig',)
else:
    INSTALLED_APPS += ('anylink',)

ANYLINK_EXTENSIONS = (
    'anylink.extensions.ExternalLink',
    ('anylink.extensions.ModelLink', {'model': 'testproject.LinkableObject'}),
)

STATIC_URL = '/static/'

ANYLINK_ALLOW_MULTIPLE_USE = False
