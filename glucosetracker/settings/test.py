"""
Test settings and globals which allow us to run our test suite locally.
"""

from .base import *

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'akr2icmg1n8%z^3fe3c+)5d0(t^cy-2_25rrl35a7@!scna^1#'

########## IN-MEMORY TEST DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}