from os import environ

if 'DEBUG' not in environ or not environ['DEBUG']:
    from .production import *
else:
    from .development import *
