from django.urls import path
from wagtail import hooks
from wagtail.admin.menu import MenuItem


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
