# Vibe Turistic — схема контент-моделей (Django + Wagtail)

Этот документ — ТЗ для переноса HTML-макета на **Django + Wagtail + Tailwind**.
Цель: вся информация о турах, датах, отзывах и документах **редактируется через админку Wagtail**, ничего не захардкожено в шаблонах.

Макет (`scripts/tour-data.js`) — это прототип данных. Ниже — как те же данные ложатся на модели Wagtail.

---

## 1. Дерево страниц и снипеты

```
HomePage (главная)
├── TourIndexPage  "Туры"            (необязательно — можно вешать TourPage прямо под Home)
│   ├── TourPage   "Тур 5 дней"
│   ├── TourPage   "Тур 3 дня"
│   └── TourPage   "Индивидуальный тур" (is_custom=True, цена скрыта)
└── LegalPage      "Политика конфиденциальности"
    LegalPage      "Согласие на обработку"
    LegalPage      "Договор оферты"
    LegalPage      "Пользовательское соглашение"

Snippets (через @register_snippet):
• Departure   — заезд/дата (FK на TourPage)   → блок «Даты», «интеграция с админкой»
• Review      — отзыв
• WhyUsItem   — карточка «Почему мы»

Settings (@register_setting):
• SiteSettings — контакты, соцсети, текст cookie, счётчики (подписчики/рейтинг/отзывы)
```

---

## 2. Карта: блок дизайна → модель/поле

| Блок на странице | Источник данных | Модель / поле |
|---|---|---|
| Шапка-герой (заголовок, лента, под-текст) | HomePage | `HomePage.hero_*` |
| Карточки выбора тура (5/3/индивид.) | дочерние `TourPage` | автоматически из дерева |
| Блок «Основная информация» | TourPage | `price, prepay, group_size, meet_time, return_time` |
| «Что входит» | TourPage → инлайн | `IncludedItem (icon, text)` |
| «Что НЕ входит» | TourPage → инлайн | `NotIncludedItem (text)` |
| «Что взять с собой» | TourPage → инлайн (с дефолтом) | `PackingItem (icon, title, note)` |
| «Что важно знать» (дисклеймер) | TourPage | `important_note (RichText)` |
| Блок «Даты заездов» | snippet `Departure` | фильтр по туру, сорт. по дате |
| «Расписание» на главной | snippet `Departure` | агрегировано по месяцам |
| «Отзывы» | snippet `Review` | — |
| «Почему мы» | snippet `WhyUsItem` | — |
| Документы (футер) | `LegalPage` | дерево страниц |
| Контакты, cookie-текст, счётчики | `SiteSettings` | — |

---

## 3. Иконки

В макете иконки — это `id` из `assets/sprite.svg` (`i-bus`, `i-mountain`, `i-coffee`, `i-guide`, `i-swim`, `i-boat`, `i-star`, …).
В админке делаем это **выбором из списка**, чтобы редактор не вводил id руками:

```python
ICON_CHOICES = [
    ("i-bus", "Транспорт"), ("i-mountain", "Горы / проживание"),
    ("i-coffee", "Питание / кофе"), ("i-guide", "Гид"),
    ("i-swim", "SUP / вода"), ("i-boat", "Катер"),
    ("i-star", "Экскурсии"), ("i-hat", "Головной убор"),
    ("i-glasses", "Очки"), ("i-sun", "Крем SPF"), ("i-shoe", "Обувь"),
    ("i-umbrella", "Дождевик"), ("i-cash", "Деньги"),
    ("i-jacket", "Тёплая одежда"), ("i-battery", "Зарядка"),
    ("i-smile", "Настроение"),
]
```
В шаблоне: `<svg class="i"><use href="{% static 'sprite.svg' %}#{{ item.icon }}"></use></svg>`

---

## 4. models.py

```python
from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


# ─── Главная ────────────────────────────────────────────────
class HomePage(Page):
    hero_headline   = models.CharField("Заголовок героя", max_length=120,
                                        default="Vibe Turistic")
    hero_ribbon     = models.CharField("Лента (бейдж)", max_length=120,
                                        default="№1 молодёжные туры по Дагестану")
    hero_subtitle   = models.TextField("Подзаголовок", blank=True)
    hero_bg         = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                        on_delete=models.SET_NULL, related_name="+")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_headline"),
            FieldPanel("hero_ribbon"),
            FieldPanel("hero_subtitle"),
            FieldPanel("hero_bg"),
        ], heading="Герой"),
    ]

    def get_context(self, request):
        ctx = super().get_context(request)
        ctx["tours"]   = TourPage.objects.live().child_of(self).order_by("-duration_days")
        ctx["reviews"] = Review.objects.all()
        ctx["why"]     = WhyUsItem.objects.all()
        ctx["months"]  = Departure.objects.upcoming_by_month()  # см. менеджер ниже
        return ctx


# ─── Страница тура ──────────────────────────────────────────
class TourPage(Page):
    is_custom      = models.BooleanField("Индивидуальный (цена скрыта)", default=False)
    badge          = models.CharField("Бейдж", max_length=40, blank=True)   # «Хит сезона»
    tagline        = models.CharField("Короткое описание", max_length=200, blank=True)

    duration_days  = models.PositiveIntegerField("Дней", default=5)
    duration_label = models.CharField("Длительность", max_length=40,
                                       default="5 дней / 4 ночи")

    price          = models.DecimalField("Цена, ₽", max_digits=8, decimal_places=0,
                                         null=True, blank=True)   # null = «по запросу»
    prepay         = models.DecimalField("Предоплата, ₽", max_digits=8, decimal_places=0,
                                         null=True, blank=True)
    group_size     = models.CharField("Размер группы", max_length=40, default="до 18")
    meet_time      = models.CharField("Сбор тура", max_length=40, default="8:30")
    return_time    = models.CharField("Вылет обратно", max_length=40, default="после 20:00")

    hero_image     = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name="+")
    card_image     = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name="+")
    included_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name="+")
    excluded_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name="+")

    important_note = RichTextField("Что важно знать (дисклеймер)", blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("is_custom"), FieldPanel("badge"),
            FieldPanel("tagline"),
            FieldPanel("duration_days"), FieldPanel("duration_label"),
        ], heading="Основное"),
        MultiFieldPanel([
            FieldPanel("price"), FieldPanel("prepay"),
            FieldPanel("group_size"),
            FieldPanel("meet_time"), FieldPanel("return_time"),
        ], heading="Цена и условия"),
        MultiFieldPanel([
            FieldPanel("hero_image"), FieldPanel("card_image"),
            FieldPanel("included_image"), FieldPanel("excluded_image"),
        ], heading="Изображения"),
        InlinePanel("included_items",  heading="Что входит"),
        InlinePanel("excluded_items",  heading="Что НЕ входит"),
        InlinePanel("packing_items",   heading="Что взять с собой"),
        FieldPanel("important_note"),
    ]

    @property
    def departures(self):
        return self.departure_set.filter(date_from__gte=timezone.now()).order_by("date_from")


class IncludedItem(Orderable):
    page = ParentalKey(TourPage, related_name="included_items", on_delete=models.CASCADE)
    icon = models.CharField(max_length=30, choices=ICON_CHOICES, default="i-star")
    text = models.CharField(max_length=200)
    panels = [FieldPanel("icon"), FieldPanel("text")]


class ExcludedItem(Orderable):
    page = ParentalKey(TourPage, related_name="excluded_items", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    panels = [FieldPanel("text")]


class PackingItem(Orderable):
    page  = ParentalKey(TourPage, related_name="packing_items", on_delete=models.CASCADE)
    icon  = models.CharField(max_length=30, choices=ICON_CHOICES, default="i-star")
    title = models.CharField(max_length=80)
    note  = models.CharField(max_length=120, blank=True)
    panels = [FieldPanel("icon"), FieldPanel("title"), FieldPanel("note")]


# ─── Заезды / даты (интеграция с админкой) ──────────────────
class DepartureQuerySet(models.QuerySet):
    def upcoming_by_month(self):
        ...  # группировка по месяцу для блока «Расписание»

class Departure(models.Model):
    SEATS = [("ok", "есть места"), ("low", "мало мест"), ("full", "нет мест")]
    tour       = models.ForeignKey(TourPage, on_delete=models.CASCADE)
    date_from  = models.DateField("Начало")
    date_to    = models.DateField("Конец")
    seats_left = models.PositiveIntegerField("Осталось мест", default=18)
    status     = models.CharField(max_length=4, choices=SEATS, default="ok")
    objects = DepartureQuerySet.as_manager()

    class Meta:
        ordering = ["date_from"]
        verbose_name = "Заезд"; verbose_name_plural = "Заезды"

register_snippet(Departure)


# ─── Отзывы ─────────────────────────────────────────────────
@register_snippet
class Review(models.Model):
    name         = models.CharField(max_length=60)
    city         = models.CharField(max_length=60, blank=True)
    rating       = models.PositiveSmallIntegerField(default=5)
    tour_label   = models.CharField(max_length=40, blank=True)   # «5-дневный тур»
    text         = models.TextField()
    avatar_color = models.CharField(max_length=7, default="#28B5FF")

    @property
    def initials(self):
        return "".join(p[0] for p in self.name.split()[:2]).upper()


# ─── «Почему мы» ────────────────────────────────────────────
@register_snippet
class WhyUsItem(models.Model):
    icon  = models.CharField(max_length=30, choices=ICON_CHOICES, default="i-star")
    title = models.CharField(max_length=80)
    text  = models.TextField()
    sort  = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["sort"]


# ─── Юридические страницы ───────────────────────────────────
class LegalPage(Page):
    body = RichTextField("Текст документа")
    content_panels = Page.content_panels + [FieldPanel("body")]


# ─── Настройки сайта ────────────────────────────────────────
@register_setting
class SiteSettings(BaseSiteSetting):
    phone        = models.CharField(max_length=40, blank=True)
    telegram     = models.URLField(blank=True)
    vk           = models.URLField(blank=True)
    whatsapp     = models.URLField(blank=True)
    subscribers  = models.CharField(max_length=20, default="31,8K")
    rating       = models.CharField(max_length=10, default="5,0")
    reviews_count= models.PositiveIntegerField(default=27)
    cookie_text  = RichTextField(blank=True)
```

---

## 5. Форма брони / «Задать вопрос»

Форма (`#ask`) — обычная Django-форма или Wagtail `FormPage`. Поля макета:
`name` (required), `contact` (required), `tour` (select), `month` (select), `msg`.

Рекомендация: модель `BookingRequest` + отправка в Telegram-бот/почту через сигнал.
`tour` и `month` подтягивать динамически из `TourPage` и будущих `Departure`,
а не хардкодить `<option>`.

---

## 6. Tailwind CSS

Дизайн-токены из `styles/vibe.css` переносятся в `tailwind.config.js`:

```js
theme: {
  extend: {
    colors: {
      sky:  { DEFAULT: '#12A2F2', deep: '#0B6FD0', darker: '#0A4FA0' },
      neon: { DEFAULT: '#FFE000', deep: '#F4C400' },
      ink:  { DEFAULT: '#0A1E33', 2: '#13314F' },
      pop:  '#FF4D8D',
    },
    borderRadius: { sm:'14px', md:'22px', lg:'34px', xl:'46px' },
    fontFamily: {
      display: ['Unbounded', 'sans-serif'],
      body:    ['Manrope', 'sans-serif'],
      script:  ['Caveat', 'cursive'],
    },
  },
}
```

Компонентные стили (кнопки, карточки, чек-листы) удобно вынести в `@layer components`
(`.btn`, `.tcard`, `.infocard` и т.д.) — это 1:1 классы из текущего `vibe.css`,
их не нужно переписывать в utility-формат. Тема (`data-palette`) реализуется через
CSS-переменные, как сейчас, либо через Tailwind-плагин.

---

## 7. Соответствие прототипа и моделей

| `tour-data.js` | Модель Wagtail |
|---|---|
| `TOURS['5']`, `TOURS['3']` | две `TourPage` |
| `TOURS.x.included[]` | `IncludedItem` (инлайн) |
| `NOT_INCLUDED[]` | `ExcludedItem` (инлайн; общий дефолт можно засидить) |
| `TAKE[]` | `PackingItem` (инлайн; дефолт-набор) |
| `SCHED[]` | `Departure` (snippet) |
| `REVIEWS[]` | `Review` (snippet) |
| блок «Почему мы» (статичен в HTML) | `WhyUsItem` (snippet) |
| тексты документов (`docs/*.html`) | `LegalPage` |
| счётчики 31,8K / 5,0 / 27 | `SiteSettings` |

> Шаблоны Wagtail повторяют разметку из `Vibe Travel.html` / `tours/tour-*.html`,
> заменяя JS-рендер (`tour-data.js`) на `{% for %}` по объектам выше.
> Иконки и спрайт (`assets/sprite.svg`), `styles/vibe.css` переносятся как есть.
