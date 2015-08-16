from .base import *

# Debug config
DEBUG = False
# End debug config

# Hosts
ALLOWED_HOSTS = ['*']
# End hosts

# Database
# example:  postgres://USER:PASSWORD@HOST:PORT/NAME
DATABASES = {'default': dj_database_url.config(
    default='postgres://postgres@db:5432/postgres')}
# End Database

# Sorl-Thumbnail
THUMBNAIL_REDIS_HOST = 'redis'
# End Sorl-Thumbnail

# Redis
CACHES['default']['LOCATION'] = 'redis:6379'
# End Redis
