import json
import os
import urllib.request
import urllib.error
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
    tour      = data.get("tour", "").strip()
    departure = data.get("departure", "")
    msg       = data.get("msg", "").strip()

    if not name or not contact:
        return JsonResponse({"ok": False, "error": "Имя и контакт обязательны"}, status=400)

    from tours.models import Departure as Dep, BookingLead, TourPage

    tour_name = tour
    if tour:
        try:
            tour_name = TourPage.objects.get(pk=tour).title
        except Exception:
            pass

    dep_label = ""
    if departure:
        try:
            d = Dep.objects.get(pk=departure)
            dep_label = f"{d.date_from} – {d.date_to}"
        except Dep.DoesNotExist:
            dep_label = departure

    BookingLead.objects.create(
        name=name,
        contact=contact,
        email=email,
        tour_name=tour_name,
        departure_label=dep_label,
        msg=msg,
    )

    survey_id = os.getenv("SURVEY_ID")
    token = os.getenv("YANDEX_FORMS_TOKEN")
    if survey_id and token:
        url = f"https://api.forms.yandex.net/v1/surveys/{survey_id}/form"
        payload = {
            "name": name,
            "phone": contact,
            "email": email,
            "tour": tour_name,
            "departure": dep_label,
            "coment": msg,
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"OAuth {token}",
                },
            )
            with urllib.request.urlopen(req) as response:
                response.read()
        except Exception:
            pass

    return JsonResponse({"ok": True, "message": "Спасибо! Мы свяжемся с вами в ближайшую минуту 🐑"})
