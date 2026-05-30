from .base import *

DEBUG = True

SECRET_KEY = "django-insecure-&#o^3_2-5guci2bq)&e6nv(9jf!p$00v0kbod&)vffzgn9(o!h"

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass
