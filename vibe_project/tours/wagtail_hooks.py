from wagtail import hooks
from wagtail.admin.menu import MenuItem
from django.urls import reverse


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "wagtailadmin/icons/doc-full-inverse.svg",
        "wagtailadmin/icons/suitcase.svg",
        "wagtailadmin/icons/calendar.svg",
        "wagtailadmin/icons/star-empty.svg",
        "wagtailadmin/icons/tick.svg",
        "wagtailadmin/icons/cross.svg",
        "wagtailadmin/icons/user.svg",
        "wagtailadmin/icons/group.svg",
        "wagtailadmin/icons/mail.svg",
        "wagtailadmin/icons/placeholder.svg",
    ]
