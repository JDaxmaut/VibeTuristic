from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from tours.views import booking_submit

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("booking/submit/", booking_submit, name="booking_submit"),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

# Serve media files in dev regardless of DEBUG.
# django.conf.urls.static.static() silently returns [] when DEBUG=False,
# so we wire up the serve view directly. Replace with nginx/S3 in production.
from django.urls import re_path
from django.views.static import serve as _serve
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", _serve, {"document_root": settings.MEDIA_ROOT}),
]

urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
