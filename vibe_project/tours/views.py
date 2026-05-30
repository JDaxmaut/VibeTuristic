import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def booking_submit(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    name      = data.get("name", "").strip()
    contact   = data.get("contact", "").strip()
    email     = data.get("email", "").strip()
    tour      = data.get("tour", "")
    departure = data.get("departure", "")
    msg       = data.get("msg", "")

    if not name or not contact:
        return JsonResponse({"ok": False, "error": "Имя и контакт обязательны"}, status=400)

    from tours.models import Departure as Dep
    dep_label = ""
    if departure:
        try:
            d = Dep.objects.get(pk=departure)
            dep_label = f"{d.date_from} – {d.date_to} ({d.tour.title})"
        except Dep.DoesNotExist:
            dep_label = departure

    print("=== Новая заявка ===")
    print(f"Имя: {name}")
    print(f"Контакт: {contact}")
    print(f"E-mail: {email}")
    print(f"Тур: {tour}")
    print(f"Заезд: {dep_label}")
    print(f"Сообщение: {msg}")

    return JsonResponse({"ok": True, "message": "Спасибо! Мы свяжемся с вами в ближайшую минуту 🐑"})
