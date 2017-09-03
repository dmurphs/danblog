from .base import *

# Debug config
DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
# End Debug config

# Hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# End Hosts


# Django Debug Toolbar config
INSTALLED_APPS += (
    'debug_toolbar', )

INTERNAL_IPS = ('127.0.0.1', 'localhost')
# End Django Debug Toolbar config

# Database
# example:  postgres://USER:PASSWORD@HOST:PORT/NAME
DATABASES = {'default': dj_database_url.config(
    default='postgres:///danblog')}
# End Database

# Secret key
SECRET_KEY = u"ga=sq!5ysyq8#3)-ait(0q%c1*-0xhuk=1c!+q_te+=b(m-21*"
# End secret key