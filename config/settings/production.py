from .base import *

DEBUG = True

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

try:
    from .local import *
except ImportError:
    pass
