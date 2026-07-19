import os
from datetime import date

from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.ui.components import Component
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import BookingLead, Departure, HomePage, TourPage


# ── Admin URL helper ──────────────────────────────────────────
def _admin_url():
    return os.environ.get("ADMIN_URL", "vibe-admin/")


# ── Global admin CSS ──────────────────────────────────────────
@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}?v=4">',
        static("css/wagtail_admin.css"),
    )


# ── Dashboard panels ──────────────────────────────────────────
class QuickActionsPanel(Component):
    name = "quick_actions"
    order = 49

    def render_html(self, parent_context=None):
        home = HomePage.objects.first()
        html = render_to_string("wagtailadmin/panels/quick_actions.html", {
            "home_id": home.pk if home else None,
            "admin_url": _admin_url(),
        })
        return mark_safe(html)


class DraftToursPanel(Component):
    name = "draft_tours"
    order = 50

    def render_html(self, parent_context=None):
        drafts = TourPage.objects.filter(live=False).order_by("title")
        if not drafts.exists():
            return mark_safe("")
        html = render_to_string("wagtailadmin/panels/draft_tours.html", {
            "drafts": drafts,
            "admin_url": _admin_url(),
        })
        return mark_safe(html)


class UpcomingDatesPanel(Component):
    name = "upcoming_dates"
    order = 51

    def render_html(self, parent_context=None):
        dates = (
            Departure.objects
            .filter(date_from__gte=date.today())
            .select_related("tour")
            .order_by("date_from")[:8]
        )
        html = render_to_string("wagtailadmin/panels/upcoming_dates.html", {
            "dates": dates,
            "admin_url": _admin_url(),
        })
        return mark_safe(html)


@hooks.register("construct_homepage_panels")
def customize_homepage_panels(request, panels):
    keep = {"site_summary"}
    panels[:] = [p for p in panels if getattr(p, "name", None) in keep]
    panels.insert(0, QuickActionsPanel())
    panels.insert(1, DraftToursPanel())
    panels.append(UpcomingDatesPanel())


# ── Tours admin view ──────────────────────────────────────────
def tours_admin_view(request):
    home = HomePage.objects.first()
    all_tours = TourPage.objects.all().order_by("title")
    return render(request, "wagtailadmin/tours_list.html", {
        "live_tours":  [t for t in all_tours if t.live],
        "draft_tours": [t for t in all_tours if not t.live],
        "home_id": home.pk if home else None,
        "admin_url": _admin_url(),
    })


# ── Quick-save dates endpoint ─────────────────────────────────
@csrf_exempt
@require_POST
def quick_save_dates(request):
    dates = Departure.objects.filter(date_from__gte=date.today())
    for d in dates:
        changed = False
        if f"seats_{d.pk}" in request.POST:
            try:
                d.seats_left = max(0, int(request.POST[f"seats_{d.pk}"]))
                changed = True
            except ValueError:
                pass
        if f"status_{d.pk}" in request.POST:
            new_status = request.POST[f"status_{d.pk}"]
            if new_status in ("ok", "low", "full"):
                d.status = new_status
                changed = True
        if changed:
            d.save()
    return HttpResponseRedirect(f"/{_admin_url()}")


# ── Admin URLs ────────────────────────────────────────────────
@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("quick-save-dates/", quick_save_dates, name="quick_save_dates"),
        path("moi-tury/", tours_admin_view, name="tours_admin_list"),
        path("docs/", _docs_view, name="admin_docs"),
    ]


def _docs_view(request):
    return render(request, "tours/admin_docs.html")


# ── Menu items ────────────────────────────────────────────────
@hooks.register("register_admin_menu_item")
def register_tours_menu_item():
    return MenuItem(
        "Мои туры",
        f"/{_admin_url()}moi-tury/",
        icon_name="list-ul",
        order=200,
    )


@hooks.register("register_admin_menu_item")
def register_docs_menu_item():
    return MenuItem(
        "Справка",
        reverse("admin_docs"),
        icon_name="help",
        order=9999,
    )


# ── Page listing: «Открыть» button for TourPage ──────────────
@hooks.register("construct_page_listing_buttons")
def add_open_button(buttons, page, user, context=None):
    from wagtail.admin.widgets import PageListingButton
    if isinstance(page, TourPage) and page.live:
        buttons.append(PageListingButton(
            "Открыть",
            page.url,
            attrs={"target": "_blank", "rel": "noopener"},
            priority=20,
        ))


# ── Clean up menu ─────────────────────────────────────────────
@hooks.register("construct_main_menu")
def hide_menu_items(request, menu_items):
    remove = {"help", "reports"}
    menu_items[:] = [i for i in menu_items if i.name not in remove]


@hooks.register("construct_settings_menu")
def hide_settings_items(request, menu_items):
    remove = {"workflows", "workflow-tasks"}
    menu_items[:] = [i for i in menu_items if i.name not in remove]


# ── BookingLead snippet ───────────────────────────────────────
class BookingLeadViewSet(SnippetViewSet):
    model = BookingLead
    icon = "mail"
    menu_label = "Заявки"
    menu_order = 100
    list_display = ["name", "contact", "email", "tour_name", "departure_label", "created_at"]
    search_fields = ["name", "contact", "email"]
    ordering = ["-created_at"]


register_snippet(BookingLeadViewSet)
