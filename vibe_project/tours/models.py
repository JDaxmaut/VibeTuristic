from django.db import models
from django.utils import timezone
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel,
    TabbedInterface, ObjectList,
)
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from modelcluster.fields import ParentalKey


ICON_CHOICES = [
    ("i-bus", "Транспорт"),
    ("i-mountain", "Горы / проживание"),
    ("i-coffee", "Питание / кофе"),
    ("i-guide", "Гид"),
    ("i-swim", "SUP / вода"),
    ("i-boat", "Катер"),
    ("i-star", "Экскурсии"),
    ("i-hat", "Головной убор"),
    ("i-glasses", "Очки"),
    ("i-sun", "Крем SPF"),
    ("i-shoe", "Обувь"),
    ("i-umbrella", "Дождевик"),
    ("i-cash", "Деньги"),
    ("i-jacket", "Тёплая одежда"),
    ("i-battery", "Зарядка"),
    ("i-smile", "Настроение"),
]


class HomePage(Page):
    template = "home/home_page.html"

    hero_headline = models.CharField(
        "Заголовок героя", max_length=120, default="Vibe Turistic"
    )
    hero_ribbon = models.CharField(
        "Лента (бейдж)", max_length=120, default="№1 молодёжные туры по Дагестану"
    )
    hero_subtitle = models.TextField("Подзаголовок", blank=True)
    hero_bg = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_headline"),
                FieldPanel("hero_ribbon"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_bg"),
            ],
            heading="Герой",
        ),
    ]

    def get_context(self, request):
        from collections import defaultdict

        ctx = super().get_context(request)

        # select_related('card_image') prevents N+1 FK hits in template
        tours = list(
            TourPage.objects.live()
            .child_of(self)
            .select_related("card_image")
            .order_by("-duration_days")
        )
        ctx["tours"] = tours
        ctx["reviews"] = Review.objects.all()
        ctx["why_items"] = WhyUsItem.objects.all()
        ctx["legal_pages"] = LegalPage.objects.live()

        # Single query for ALL upcoming departures — covers both schedule
        # display and the booking-form JSON payload (no per-tour sub-queries)
        upcoming = list(
            Departure.objects.upcoming()
            .select_related("tour")
            .order_by("date_from")
        )

        months = defaultdict(list)
        for d in upcoming:
            months[(d.date_from.year, d.date_from.month)].append(d)
        ctx["schedule"] = sorted(months.items())

        tour_ids = {t.pk for t in tours}
        tours_dep = {str(t.pk): [] for t in tours}
        for d in upcoming:
            if d.tour_id in tour_ids:
                tours_dep[str(d.tour_id)].append({
                    "value": str(d.pk),
                    "from": d.date_from.isoformat(),
                    "to": d.date_to.isoformat(),
                    "status": d.status,
                })
        ctx["tours_departures"] = tours_dep
        return ctx


class TourPage(Page):
    is_custom = models.BooleanField("Индивидуальный (цена скрыта)", default=False)
    badge = models.CharField("Бейдж", max_length=40, blank=True)
    tagline = models.CharField("Короткое описание", max_length=200, blank=True, default="")

    duration_days = models.PositiveIntegerField("Дней", default=5)
    duration_label = models.CharField(
        "Длительность", max_length=40, default="5 дней / 4 ночи"
    )

    price = models.DecimalField(
        "Цена, ₽", max_digits=8, decimal_places=0, null=True, blank=True
    )
    prepay = models.DecimalField(
        "Предоплата, ₽", max_digits=8, decimal_places=0, null=True, blank=True
    )
    group_size = models.CharField("Размер группы", max_length=40, default="до 18")
    meet_time = models.CharField("Сбор тура", max_length=40, default="8:30", blank=True)
    return_time = models.CharField(
        "Вылет обратно", max_length=40, default="после 20:00", blank=True
    )

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    card_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    included_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    excluded_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    description = RichTextField("Описание тура", blank=True)
    important_note = RichTextField("Что важно знать (дисклеймер)", blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("is_custom"),
                FieldPanel("badge"),
                FieldPanel("tagline"),
                FieldPanel("duration_days"),
                FieldPanel("duration_label"),
            ],
            heading="Основное",
        ),
        MultiFieldPanel(
            [
                FieldPanel("price"),
                FieldPanel("prepay"),
                FieldPanel("group_size"),
                FieldPanel("meet_time"),
                FieldPanel("return_time"),
            ],
            heading="Цена и условия",
        ),
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("card_image"),
                FieldPanel("included_image"),
                FieldPanel("excluded_image"),
            ],
            heading="Изображения",
        ),
        FieldPanel("description"),
        InlinePanel("itinerary_days", heading="Программа по дням"),
        InlinePanel("included_items", heading="Что входит"),
        InlinePanel("excluded_items", heading="Что НЕ входит"),
        InlinePanel("packing_items", heading="Что взять с собой"),
        FieldPanel("important_note"),
        InlinePanel("gallery_photos", heading="Фотогалерея"),
    ]

    schedule_panels = [
        InlinePanel(
            "departure_set",
            heading="Заезды тура",
            label="Заезд",
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Содержимое"),
        ObjectList(schedule_panels, heading="Расписание"),
        ObjectList(Page.promote_panels, heading="Продвижение"),
    ])

    @property
    def departures(self):
        return self.departure_set.filter(date_from__gte=timezone.now()).order_by(
            "date_from"
        )


class IncludedItem(Orderable):
    page = ParentalKey(
        TourPage, related_name="included_items", on_delete=models.CASCADE
    )
    icon = models.CharField(
        "Иконка", max_length=30, choices=ICON_CHOICES, default="i-star"
    )
    text = models.CharField("Текст", max_length=200)

    panels = [FieldPanel("icon"), FieldPanel("text")]

    def __str__(self):
        return self.text


class ExcludedItem(Orderable):
    page = ParentalKey(
        TourPage, related_name="excluded_items", on_delete=models.CASCADE
    )
    text = models.CharField("Текст", max_length=200)

    panels = [FieldPanel("text")]

    def __str__(self):
        return self.text


class PackingItem(Orderable):
    page = ParentalKey(
        TourPage, related_name="packing_items", on_delete=models.CASCADE
    )
    icon = models.CharField(
        "Иконка", max_length=30, choices=ICON_CHOICES, default="i-star"
    )
    title = models.CharField("Название", max_length=80)
    note = models.CharField("Подсказка", max_length=120, blank=True)

    panels = [FieldPanel("icon"), FieldPanel("title"), FieldPanel("note")]

    def __str__(self):
        return self.title


class TourGalleryPhoto(Orderable):
    page = ParentalKey(
        TourPage, related_name="gallery_photos", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Фото",
    )
    caption = models.CharField("Подпись", max_length=200, blank=True)

    panels = [FieldPanel("image"), FieldPanel("caption")]

    def __str__(self):
        return self.caption or str(self.image)


class ItineraryDay(Orderable):
    page = ParentalKey(
        TourPage, related_name="itinerary_days", on_delete=models.CASCADE
    )
    title = models.CharField("Заголовок дня", max_length=200)
    subtitle = models.CharField("Краткое описание (под заголовком)", max_length=200, blank=True)
    description = RichTextField("Описание дня")

    panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "День маршрута"
        verbose_name_plural = "Дни маршрута"

    def __str__(self):
        return self.title


class DepartureQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(date_from__gte=timezone.now())

    def upcoming_by_month(self):
        from django.db.models.functions import TruncMonth

        return (
            self.upcoming()
            .annotate(month=TruncMonth("date_from"))
            .order_by("month")
            .distinct("month")
        )


@register_snippet
class Departure(models.Model):
    SEATS = [
        ("ok", "есть места"),
        ("low", "мало мест"),
        ("full", "нет мест"),
    ]

    # ParentalKey is required for InlinePanel on TourPage
    tour = ParentalKey(TourPage, on_delete=models.CASCADE, verbose_name="Тур",
                       related_name="departure_set")
    date_from = models.DateField("Начало")
    date_to = models.DateField("Конец")
    seats_left = models.PositiveIntegerField("Осталось мест", default=18)
    status = models.CharField(
        max_length=4, choices=SEATS, default="ok", verbose_name="Статус"
    )

    objects = DepartureQuerySet.as_manager()

    panels = [
        MultiFieldPanel([
            FieldPanel("date_from"),
            FieldPanel("date_to"),
        ], heading="Даты заезда"),
        FieldPanel("seats_left"),
        FieldPanel("status"),
    ]

    class Meta:
        ordering = ["date_from"]
        verbose_name = "Заезд"
        verbose_name_plural = "Заезды"

    def __str__(self):
        return f"{self.date_from} – {self.date_to}"


@register_snippet
class Review(models.Model):
    name = models.CharField("Имя", max_length=60)
    city = models.CharField("Город", max_length=60, blank=True)
    rating = models.PositiveSmallIntegerField("Рейтинг", default=5)
    tour_label = models.CharField(
        "Метка тура", max_length=40, blank=True
    )
    text = models.TextField("Текст отзыва")
    avatar_color = models.CharField(
        "Цвет аватара", max_length=7, default="#28B5FF"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.name} — {self.tour_label}"

    @property
    def initials(self):
        return "".join(p[0] for p in self.name.split()[:2]).upper()


@register_snippet
class WhyUsItem(models.Model):
    THEME_CHOICES = [
        ("prog", "Синий"),
        ("sched", "Жёлтый"),
        ("rev", "Розовый"),
        ("why", "Зелёный"),
        ("ask", "Фиолетовый"),
    ]

    icon = models.CharField(
        max_length=30, choices=ICON_CHOICES, default="i-star"
    )
    theme = models.CharField(
        "Цвет иконки", max_length=10, choices=THEME_CHOICES, default="prog"
    )
    title = models.CharField("Заголовок", max_length=80)
    text = models.TextField("Текст")
    sort = models.PositiveIntegerField("Порядок", default=0)

    panels = [FieldPanel("icon"), FieldPanel("theme"), FieldPanel("title"), FieldPanel("text")]

    class Meta:
        ordering = ["sort"]
        verbose_name = "Почему мы"
        verbose_name_plural = "Почему мы"

    def __str__(self):
        return self.title


class LegalPage(Page):
    template = "tours/legal_page.html"
    body = RichTextField("Текст документа")

    content_panels = Page.content_panels + [FieldPanel("body")]

    class Meta:
        verbose_name = "Юридическая страница"
        verbose_name_plural = "Юридические страницы"


@register_setting
class SiteSettings(BaseSiteSetting):
    phone = models.CharField("Телефон", max_length=40, blank=True)
    telegram = models.URLField("Telegram", blank=True)
    vk = models.URLField("VK", blank=True)
    whatsapp = models.URLField("WhatsApp", blank=True)
    subscribers = models.CharField(
        "Подписчики", max_length=20, default="31,8K"
    )
    rating = models.CharField("Рейтинг", max_length=10, default="5,0")
    reviews_count = models.PositiveIntegerField("Кол-во отзывов", default=27)
    cookie_text = RichTextField("Текст cookie-баннера", blank=True)

    class Meta:
        verbose_name = "Настройки сайта"
