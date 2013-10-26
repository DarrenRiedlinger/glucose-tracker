from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'glucosetracker',
        'USER': 'developer',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

INSTALLED_APPS += ('debug_toolbar', )
INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES += \
    ('debug_toolbar.middleware.DebugToolbarMiddleware', )

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS':False,
    'SHOW_TEMPLATE_CONTEXT':True,
    'HIDE_DJANGO_SQL':False,
}
