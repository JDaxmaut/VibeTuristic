from django.contrib import admin
from .models import BookingLead


@admin.register(BookingLead)
class BookingLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "email", "tour_name", "departure_label", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "contact", "email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
