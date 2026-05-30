from django import template

register = template.Library()


@register.filter
def rub(value):
    if value is None or value == "":
        return ""
    try:
        n = int(round(float(value)))
    except (TypeError, ValueError):
        return value
    return f"{n:,}".replace(",", "\u00a0")


@register.simple_tag
def get_legal_pages():
    from tours.models import LegalPage
    return LegalPage.objects.live()
