from django.db import migrations

INCLUDED = [
    ("i-bus",      "Транспорт на все дни тура"),
    ("i-mountain", "Проживание в гостевом доме в горах"),
    ("i-coffee",   "Питание: завтраки, обеды, ужины"),
    ("i-guide",    "Услуги профессионального гида"),
    ("i-swim",     "Катание на SUP-борде на Каспийском море"),
    ("i-boat",     "Прогулка на катере"),
    ("i-star",     "Все экскурсии по программе тура"),
    ("i-coffee",   "Квадро-байк на барханах"),
]

EXCLUDED = [
    "Авиа- или ж/д-билеты до Махачкалы и обратно",
    "Личные расходы на алкоголь",
    "Страховка",
    "Бары и рестораны вне программы тура",
    "Профессиональное фото/видео",
    "Услуги, не указанные в программе",
]


def seed(apps, schema_editor):
    HomePage = apps.get_model("tours", "HomePage")
    HomeIncludedItem = apps.get_model("tours", "HomeIncludedItem")
    HomeExcludedItem = apps.get_model("tours", "HomeExcludedItem")

    home = HomePage.objects.filter(live=True).first()
    if not home:
        return

    for i, (icon, text) in enumerate(INCLUDED):
        HomeIncludedItem.objects.create(page=home, icon=icon, text=text, sort_order=i)

    for i, text in enumerate(EXCLUDED):
        HomeExcludedItem.objects.create(page=home, text=text, sort_order=i)


def unseed(apps, schema_editor):
    HomeIncludedItem = apps.get_model("tours", "HomeIncludedItem")
    HomeExcludedItem = apps.get_model("tours", "HomeExcludedItem")
    HomeIncludedItem.objects.filter(text__in=[t for _, t in INCLUDED]).delete()
    HomeExcludedItem.objects.filter(text__in=EXCLUDED).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0008_home_included_excluded"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
