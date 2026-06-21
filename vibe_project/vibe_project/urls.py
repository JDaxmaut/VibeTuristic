import os

from django.conf import settings
from django.urls import include, path
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

from search import views as search_views
from tours.views import booking_submit

# Hidden admin URL — set ADMIN_URL env var to a secret path in production.
# Must end with a slash, e.g. "xK9mQ2pL/".
_admin_url = os.environ.get("ADMIN_URL", "vibe-admin/")

urlpatterns = [
    path(_admin_url, include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("booking/submit/", booking_submit, name="booking_submit"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap),
]

if not settings.MEDIA_URL.startswith("http"):
    from django.urls import re_path
    from django.views.static import serve as _serve
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", _serve, {"document_root": settings.MEDIA_ROOT}),
    ]

urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]
