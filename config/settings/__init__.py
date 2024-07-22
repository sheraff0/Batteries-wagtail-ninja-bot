from .env import *

from .base import *
from .installed_apps import *
from .middleware import *
from .database import *
from .email import *
from .locale import *
from .templates import *

from .company import *
from .debug_toolbar import *
#from .rest_framework import *
from .wagtail import *

from .aqsi import *

if S3_STORAGE:
    from .s3 import *

from .tg_bot import *
