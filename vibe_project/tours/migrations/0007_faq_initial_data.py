from django.db import migrations


FAQ_ITEMS = [
    {
        "question": "Может ли программа тура измениться?",
        "answer": (
            "<p>Маршрут и график посещения локаций могут быть изменены в зависимости от погодных условий. "
            "Список локаций является ориентировочным, и порядок их посещения может быть скорректирован. "
            "Просим быть готовыми к возможным изменениям и понимать это!</p>"
        ),
    },
    {
        "question": "Условия проживания?",
        "answer": (
            "<p>Проживаем в горах в гостевом доме, размещение 2-х и 3-х местное. "
            "Если поедете вдвоём — заселим в двухместный номер.</p>"
            "<p>В каждом номере свой душ/санузел + банные принадлежности. "
            "Все наши гостевые дома отличного уровня!</p>"
        ),
    },
    {
        "question": "Откуда начинается тур?",
        "answer": (
            "<p>Встречаем в Махачкале в <strong>8:30 утра</strong>. В Махачкалу лучше приехать за сутки до тура — "
            "остановиться в отеле или снять квартиру (с выбором отеля подскажем по цене/качеству).</p>"
            "<p>Два места сбора:</p>"
            "<ol>"
            "<li><strong>Аэропорт</strong> — если прилетаете в день тура, заберём в 7:45.</li>"
            "<li><strong>Южная автостанция</strong> — если приезжаете заранее.</li>"
            "</ol>"
            "<p>Такси по городу 150–200 ₽ (Яндекс).</p>"
            "<p>Привозим обратно в Махачкалу в <strong>18:00–18:30</strong>. Если планируете улететь в тот же день — "
            "билеты лучше брать после 20:00 (отвезём в аэропорт).</p>"
        ),
    },
]


def add_faq_items(apps, schema_editor):
    HomePage = apps.get_model("tours", "HomePage")
    FAQItem = apps.get_model("tours", "FAQItem")

    home = HomePage.objects.filter(live=True).first()
    if not home:
        return

    for i, item in enumerate(FAQ_ITEMS):
        FAQItem.objects.create(
            page=home,
            question=item["question"],
            answer=item["answer"],
            sort_order=i,
        )


def remove_faq_items(apps, schema_editor):
    FAQItem = apps.get_model("tours", "FAQItem")
    FAQItem.objects.filter(question__in=[f["question"] for f in FAQ_ITEMS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0006_faq_item"),
    ]

    operations = [
        migrations.RunPython(add_faq_items, remove_faq_items),
    ]
