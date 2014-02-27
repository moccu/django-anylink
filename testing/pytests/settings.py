DEBUG = True
TEMPLATE_DEBUG = True

SECRET_KEY = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'anylink'
)

ANYLINK_EXTENSIONS = (
    'anylink.extensions.ExternalLink',
)

STATIC_URL = '/static/'
