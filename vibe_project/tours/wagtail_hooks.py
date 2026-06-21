from django.urls import path
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet


@hooks.register("register_admin_urls")
def register_admin_urls():
    from . import admin_views
    return [
        path("docs/", admin_views.docs_view, name="admin_docs"),
    ]


@hooks.register("register_admin_menu_item")
def register_docs_menu_item():
    return MenuItem(
        label="Справка",
        url="/admin/docs/",
        icon_name="help",
        order=9999,
    )


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("css/wagtail_admin.css"),
    )


from .models import BookingLead


class BookingLeadViewSet(SnippetViewSet):
    model = BookingLead
    icon = "mail"
    menu_label = "Заявки"
    menu_order = 100
    list_display = ["name", "contact", "email", "tour_name", "departure_label", "created_at"]
    search_fields = ["name", "contact", "email"]
    ordering = ["-created_at"]


register_snippet(BookingLeadViewSet)
