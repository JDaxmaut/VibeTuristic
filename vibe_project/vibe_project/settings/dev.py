from .base import *

DEBUG = False

SECRET_KEY = "django-insecure-&#o^3_2-5guci2bq)&e6nv(9jf!p$00v0kbod&)vffzgn9(o!h"

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["https://vibeturistic.ru", "https://www.vibeturistic.ru"]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass
