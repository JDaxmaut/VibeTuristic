"""
Кастомные шаблонные фильтры для туров.
Положите файл в:  <app>/templatetags/tour_extras.py
(не забудьте пустой __init__.py рядом).

Использование в шаблоне:
    {% load tour_extras %}
    {{ page.price|rub }}      →  42 000
"""
from django import template

register = template.Library()


@register.filter
def rub(value):
    """Форматирует число с пробелом как разделителем тысяч: 42000 → '42 000'.
    Пустое значение → '' (чтобы можно было показать «Цена по запросу»)."""
    if value is None or value == "":
        return ""
    try:
        n = int(round(float(value)))
    except (TypeError, ValueError):
        return value
    return f"{n:,}".replace(",", "\u00a0")  # неразрывный пробел
