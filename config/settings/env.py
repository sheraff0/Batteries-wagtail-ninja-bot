import os
import sys
import environ
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env(DEBUG=(bool, False))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DEBUG', False)
TOOLBAR = env.bool('TOOLBAR', False)
SILK = env.bool('SILK', False)
SWAGGER = env.bool('SWAGGER', False)
S3_STORAGE = env.bool('S3_STORAGE', False)
DAPHNE = env.bool('DAPHNE', False)

MEDIA_BASE_URL = env('MEDIA_BASE_URL')

TESTING_MODE = 'test' in sys.argv

REDIS_URL = env('REDIS_URL')
REDIS_HOST, REDIS_PORT = re.search(r"^.*//(.+):(\d+).*$", REDIS_URL).groups()

YANDEX_METRIKA = env.bool("YANDEX_METRIKA", False)
