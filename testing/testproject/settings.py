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
    'anylink',
    'testing.testproject'
)

ANYLINK_EXTENSIONS = (
    'anylink.extensions.ExternalLink',
    ('anylink.extensions.ModelLink', {'model': 'testproject.LinkableObject'}),
)

STATIC_URL = '/static/'
