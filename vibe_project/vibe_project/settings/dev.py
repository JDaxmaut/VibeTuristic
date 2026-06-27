from .base import *

DEBUG = True

SECRET_KEY = "django-insecure-&#o^3_2-5guci2bq)&e6nv(9jf!p$00v0kbod&)vffzgn9(o!h"

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["https://*.tuna.am", "https://*.ngrok.io", "https://*.ngrok-free.app", "http://localhost:8000", "http://127.0.0.1:8000"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass
