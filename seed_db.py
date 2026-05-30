import django, os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vibe_project.settings.dev")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vibe_project"))
django.setup()

from django.utils import timezone
from wagtail.models import Page, Site
from wagtail.images.models import Image
from tours.models import HomePage, TourPage, IncludedItem, ExcludedItem, PackingItem, Departure, Review, WhyUsItem, LegalPage
from tours.models import SiteSettings as TourSiteSettings

# Get or create HomePage
root = Page.objects.get(id=1)
site = Site.objects.get(is_default_site=True)

# Check if tours home page already exists
try:
    home = HomePage.objects.get(id=site.root_page_id)
except HomePage.DoesNotExist:
    home = HomePage(
        title="Home",
        slug="home",
        hero_headline="Vibe Turistic",
        hero_ribbon="№1 молодёжные туры по Дагестану",
        hero_subtitle="Горы, каньоны, водопады и барханы — без скучных автобусов. Только вайб, движ и виды, от которых захватывает дух.",
    )
    root.add_child(instance=home)
    home.save()
    site.root_page = home
    site.save()
    print("Created HomePage")

# Clear only data without attached media (preserve TourPage gallery photos)
Departure.objects.all().delete()
Review.objects.all().delete()
WhyUsItem.objects.all().delete()
LegalPage.objects.all().delete()

print("Cleared old data (tours preserved)")

# Create TourPages
tours_data = [
    {
        "title": "Зимний тур 5 дней",
        "slug": "tour-5-days",
        "is_custom": False,
        "badge": "Хит сезона",
        "tagline": "Полное погружение в Дагестан: горы, каньоны, водопады, барханы и вода — максимум впечатлений и новые друзья.",
        "duration_days": 5,
        "duration_label": "5 дней / 4 ночи",
        "price": 42000,
        "prepay": 15000,
        "group_size": "до 18",
        "meet_time": "8:30",
        "return_time": "после 20:00",
        "included": [
            ("i-bus", "Транспорт на все 5 дней между всеми достопримечательностями"),
            ("i-mountain", "Проживание в горах 5 дней / 4 ночи в гостевом доме"),
            ("i-coffee", "Питание — полноценные завтраки, обеды и ужины"),
            ("i-guide", "Работа сертифицированного гида"),
            ("i-swim", "Прогулка на SUP-досках по водохранилищу"),
            ("i-boat", "Прогулка на катере"),
            ("i-star", "Все экскурсии и входные билеты"),
            ("i-coffee", "Кофе-тайм на природе"),
        ],
        "excluded": [
            "Авиа- или ж/д-билеты из вашего города до Махачкалы и обратно",
            "Личные траты на сувениры",
            "Спиртное",
            "Кофе и чай в кафе на остановках",
            "Экстремальные виды развлечений",
            "Всё остальное, что не указано выше",
        ],
        "packing": [
            ("i-swim", "Купальник / шорты", "для воды и SUP"),
            ("i-hat", "Головной убор", "кепка или панама"),
            ("i-glasses", "Солнцезащитные очки", "в горах ярко"),
            ("i-sun", "Солнцезащитный крем", "SPF 30+"),
            ("i-shoe", "Удобная обувь", "можно тапочки"),
            ("i-umbrella", "Дождевик", "на случай пасмурной погоды"),
            ("i-cash", "Наличные деньги", "карманные расходы"),
            ("i-jacket", "Тёплая одежда", "вечером в горах прохладно"),
            ("i-battery", "Зарядка / powerbank", "для всех гаджетов"),
            ("i-smile", "Хорошее настроение", "самое важное"),
        ],
        "important_note": "Маршрут, график и порядок посещения локаций являются ориентировочными и могут быть изменены — из-за погоды, дорожных условий или состояния группы. Поэтому важно быть готовыми к возможным изменениям и относиться к ним с пониманием: иногда самые крутые места случаются спонтанно.",
    },
    {
        "title": "Зимний тур 3 дня",
        "slug": "tour-3-days",
        "is_custom": False,
        "badge": "Уикенд",
        "tagline": "Насыщенный уикенд для тех, у кого мало времени, но много энергии — всё самое яркое за выходные.",
        "duration_days": 3,
        "duration_label": "3 дня / 2 ночи",
        "price": 33000,
        "prepay": 10000,
        "group_size": "до 18",
        "meet_time": "8:30",
        "return_time": "после 20:00",
        "included": [
            ("i-bus", "Транспорт на все 3 дня между всеми достопримечательностями"),
            ("i-mountain", "Проживание в горах 3 дня / 2 ночи в гостевом доме"),
            ("i-coffee", "Питание — полноценные завтраки, обеды и ужины"),
            ("i-guide", "Работа сертифицированного гида"),
            ("i-swim", "Прогулка на SUP-досках по водохранилищу"),
            ("i-boat", "Прогулка на катере"),
            ("i-star", "Все экскурсии и входные билеты"),
            ("i-coffee", "Кофе-тайм на природе"),
        ],
        "excluded": [
            "Авиа- или ж/д-билеты из вашего города до Махачкалы и обратно",
            "Личные траты на сувениры",
            "Спиртное",
            "Кофе и чай в кафе на остановках",
            "Экстремальные виды развлечений",
            "Всё остальное, что не указано выше",
        ],
        "packing": [
            ("i-swim", "Купальник / шорты", "для воды и SUP"),
            ("i-hat", "Головной убор", "кепка или панама"),
            ("i-glasses", "Солнцезащитные очки", "в горах ярко"),
            ("i-sun", "Солнцезащитный крем", "SPF 30+"),
            ("i-shoe", "Удобная обувь", "можно тапочки"),
            ("i-umbrella", "Дождевик", "на случай пасмурной погоды"),
            ("i-cash", "Наличные деньги", "карманные расходы"),
            ("i-jacket", "Тёплая одежда", "вечером в горах прохладно"),
            ("i-battery", "Зарядка / powerbank", "для всех гаджетов"),
            ("i-smile", "Хорошее настроение", "самое важное"),
        ],
        "important_note": "Маршрут, график и порядок посещения локаций являются ориентировочными и могут быть изменены — из-за погоды, дорожных условий или состояния группы. Поэтому важно быть готовыми к возможным изменениям и относиться к ним с пониманием: иногда самые крутые места случаются спонтанно.",
    },
    {
        "title": "Индивидуальный тур",
        "slug": "custom-tour",
        "is_custom": True,
        "badge": "Под тебя",
        "tagline": "Свои даты, свой маршрут и состав группы. Соберём тур мечты под ваш запрос.",
        "duration_label": "свои даты и маршрут",
        "price": None,
        "prepay": None,
        "group_size": "любой состав",
        "meet_time": "",
        "return_time": "",
        "included": [],
        "excluded": [],
        "packing": [],
        "important_note": "",
    },
]

tours = []
for td in tours_data:
    existing = TourPage.objects.filter(slug=td["slug"]).first()
    if existing:
        # Update basic fields, preserve gallery photos and inlines
        existing.title = td["title"]
        existing.is_custom = td["is_custom"]
        existing.badge = td.get("badge", "")
        existing.tagline = td.get("tagline", "")
        existing.duration_days = td.get("duration_days", 0)
        existing.duration_label = td.get("duration_label", "")
        existing.price = td.get("price")
        existing.prepay = td.get("prepay")
        existing.group_size = td.get("group_size", "")
        existing.meet_time = td.get("meet_time", "")
        existing.return_time = td.get("return_time", "")
        existing.important_note = td.get("important_note", "")
        existing.save()
        tours.append(existing)
        print(f"Updated tour: {existing.title}")
    else:
        tour = TourPage(
            title=td["title"],
            slug=td["slug"],
            is_custom=td["is_custom"],
            badge=td.get("badge", ""),
            tagline=td.get("tagline", ""),
            duration_days=td.get("duration_days", 0),
            duration_label=td.get("duration_label", ""),
            price=td.get("price"),
            prepay=td.get("prepay"),
            group_size=td.get("group_size", ""),
            meet_time=td.get("meet_time", ""),
            return_time=td.get("return_time", ""),
            important_note=td.get("important_note", ""),
        )
        home.add_child(instance=tour)
        tour.save()
        for icon, text in td["included"]:
            IncludedItem.objects.create(page=tour, icon=icon, text=text)
        for text in td["excluded"]:
            ExcludedItem.objects.create(page=tour, text=text)
        for icon, item, note in td["packing"]:
            PackingItem.objects.create(page=tour, icon=icon, title=item, note=note)
        tours.append(tour)
        print(f"Created tour: {tour.title}")

# Create Departures
from datetime import date
tour_3 = tours[1]
tour_5 = tours[0]
departures_data = [
    # Июнь 2026
    (date(2026, 6, 6),  date(2026, 6, 8),  tour_3, "low"),
    (date(2026, 6, 13), date(2026, 6, 17), tour_5, "ok"),
    (date(2026, 6, 20), date(2026, 6, 24), tour_5, "ok"),
    (date(2026, 6, 27), date(2026, 6, 29), tour_3, "ok"),
    # Июль 2026
    (date(2026, 7, 4),  date(2026, 7, 8),  tour_5, "full"),
    (date(2026, 7, 11), date(2026, 7, 13), tour_3, "low"),
    (date(2026, 7, 18), date(2026, 7, 22), tour_5, "ok"),
    (date(2026, 7, 25), date(2026, 7, 29), tour_5, "ok"),
    # Август 2026
    (date(2026, 8, 1),  date(2026, 8, 3),  tour_3, "ok"),
    (date(2026, 8, 8),  date(2026, 8, 12), tour_5, "low"),
    (date(2026, 8, 15), date(2026, 8, 17), tour_3, "ok"),
    (date(2026, 8, 22), date(2026, 8, 26), tour_5, "ok"),
    # Сентябрь 2026
    (date(2026, 9, 5),  date(2026, 9, 9),  tour_5, "ok"),
    (date(2026, 9, 12), date(2026, 9, 14), tour_3, "ok"),
    (date(2026, 9, 19), date(2026, 9, 23), tour_5, "ok"),
    # Октябрь 2026
    (date(2026, 10, 3),  date(2026, 10, 7),  tour_5, "ok"),
    (date(2026, 10, 10), date(2026, 10, 12), tour_3, "ok"),
    (date(2026, 10, 17), date(2026, 10, 21), tour_5, "low"),
    # Ноябрь 2026
    (date(2026, 11, 7),  date(2026, 11, 11), tour_5, "ok"),
    (date(2026, 11, 14), date(2026, 11, 16), tour_3, "ok"),
    (date(2026, 11, 21), date(2026, 11, 25), tour_5, "ok"),
]
for df, dt, tour, status in departures_data:
    Departure.objects.create(date_from=df, date_to=dt, tour=tour, status=status)
print(f"Created {len(departures_data)} departures")

# Create Reviews
reviews_data = [
    {"author_name": "Алина", "author_city": "Москва", "text": "Лучшие 5 дней за год! Гид топовый, локации космос, а группа стала семьёй уже на второй день. SUP на рассвете — отдельная любовь.", "tour_type": "5-дневный тур"},
    {"author_name": "Тимур", "author_city": "Казань", "text": "Брал короткий формат на выходные — успели нереально много. Всё чётко по организации, ни одной заминки.", "tour_type": "3-дневный тур"},
    {"author_name": "Дарья", "author_city": "СПб", "text": "Каньон, водопады, бархан — каждый день новая картинка. Рилсы залетели на сотни тысяч просмотров.", "tour_type": "5-дневный тур"},
    {"author_name": "Игорь", "author_city": "Екатеринбург", "text": "Думал будет туристический конвейер — оказалось живое приключение. Питание домашнее, порции огромные.", "tour_type": "5-дневный тур"},
    {"author_name": "Камилла", "author_city": "Уфа", "text": "Первый раз в Дагестане и сразу влюбилась. Ребята помогли с отелем до тура, всё на высшем уровне.", "tour_type": "3-дневный тур"},
    {"author_name": "Никита", "author_city": "Новосибирск", "text": "Маленькая группа — это кайф. Никакой толпы, успеваешь поговорить с гидом и реально проникнуться местом.", "tour_type": "5-дневный тур"},
    {"author_name": "Вероника", "author_city": "Краснодар", "text": "Барханы Сарыкум на закате — вау. Организация 10 из 10, вернусь летом точно.", "tour_type": "5-дневный тур"},
    {"author_name": "Артём", "author_city": "Самара", "text": "Катер, горы, кофе-тайм на скале с видом на каньон. За три дня впечатлений как за отпуск.", "tour_type": "3-дневный тур"},
]

for rd in reviews_data:
    r = Review(
        name=rd["author_name"],
        city=rd["author_city"],
        text=rd["text"],
        tour_label=rd["tour_type"],
    )
    r.save()

print(f"Created {len(reviews_data)} reviews")

# Create WhyUs items
why_data = [
    {"icon": "i-star", "theme": "prog", "title": "№1 в Дагестане по молодёжным турам", "description": "Сотни довольных гостей и рейтинг 5,0 — нам доверяют путешественники со всей страны.", "sort_order": 0},
    {"icon": "i-bus", "theme": "ask", "title": "Всё включено", "description": "Транспорт, проживание, питание и экскурсии уже в цене. Тебе остаётся только купить авиабилет — обо всём остальном позаботимся мы.", "sort_order": 1},
    {"icon": "i-guide", "theme": "prog", "title": "Гиды — местные", "description": "Знают регион как свои пять пальцев и делятся легендами, историями и секретами, которых нет в путеводителях.", "sort_order": 2},
    {"icon": "i-smile", "theme": "sched", "title": "Лагерь для взрослых", "description": "Так нас называют сами гости — ощущения, как в лучших лагерях из детства.", "sort_order": 3},
    {"icon": "i-star", "theme": "rev", "title": "Делим важные дни", "description": "Дни рождения, предложения руки и сердца — ценим, когда такие моменты доверяют нам.", "sort_order": 4},
    {"icon": "i-bus", "theme": "why", "title": "Каждый тур — семья", "description": "Создаём атмосферу, где всем уютно. Гид не просто ведёт экскурсию, а становится частью группы.", "sort_order": 5},
    {"icon": "i-hat", "theme": "prog", "title": "Безопасность", "description": "То, о чём мы думаем в первую очередь — главное в каждом нашем туре.", "sort_order": 6},
    {"icon": "i-glasses", "theme": "sched", "title": "Сотни отзывов", "description": "Сотни довольных гостей подтверждают: нам можно доверять.", "sort_order": 7},
]

for wd in why_data:
    w = WhyUsItem(
        icon=wd["icon"],
        theme=wd["theme"],
        title=wd["title"],
        text=wd["description"],
        sort=wd["sort_order"],
    )
    w.save()

print(f"Created {len(why_data)} why-us items")

# Create LegalPages
legal_data = [
    {"title": "Политика конфиденциальности", "slug": "privacy-policy", "body": "<p>Оператор: укажите наименование юридического лица или ИП, ИНН/ОГРН и юридический адрес. Контакт для обращений: info@vibeturistic.ru</p><p>Настоящая Политика конфиденциальности действует в отношении всех персональных данных, которые Оператор получает от пользователей Сайта.</p><h3>1. Какие данные мы собираем</h3><ul><li>имя и контактные данные (телефон, ник в мессенджере, e-mail), которые вы оставляете в формах бронирования и обратной связи;</li><li>технические данные: IP-адрес, тип браузера и устройства, файлы cookie, данные систем веб-аналитики;</li><li>сведения о выбранном туре и переписке с нами.</li></ul><h3>2. Цели обработки</h3><ul><li>обработка заявок на бронирование туров и обратная связь с вами;</li><li>информирование о датах заездов, акциях и изменениях в программе;</li><li>улучшение работы Сайта и качества услуг.</li></ul><h3>3. Правовые основания</h3><p>Обработка осуществляется на основании согласия субъекта персональных данных, а также для исполнения договора, в соответствии с Федеральным законом «О персональных данных» № 152-ФЗ.</p><h3>4. Передача третьим лицам</h3><p>Мы не продаём персональные данные. Данные могут передаваться партнёрам исключительно в объёме, необходимом для оказания услуги, а также уполномоченным государственным органам в случаях, предусмотренных законом.</p><h3>5. Хранение и защита</h3><p>Данные хранятся не дольше, чем требуется для целей обработки или сроков, установленных законодательством.</p><h3>6. Файлы cookie</h3><p>Сайт использует cookie для корректной работы и аналитики. Вы можете отключить cookie в настройках браузера.</p><h3>7. Ваши права</h3><p>Вы вправе запросить информацию об обработке ваших данных, потребовать их уточнения, блокирования или удаления, направив обращение на info@vibeturistic.ru.</p><h3>8. Изменения Политики</h3><p>Актуальная редакция всегда доступна на этой странице с указанием даты последнего обновления.</p>"},
    {"title": "Согласие на обработку персональных данных", "slug": "consent", "body": "<p>Настоящим я, заполняя форму на Сайте, даю согласие на обработку моих персональных данных.</p><h3>1. Перечень персональных данных</h3><p>Фамилия, имя; номер телефона; адрес электронной почты или ник в мессенджере; иные данные, добровольно указанные в формах Сайта.</p><h3>2. Цели обработки</h3><ul><li>обработка и подтверждение заявок на бронирование туров;</li><li>связь по вопросам оказания услуг;</li><li>направление информационных сообщений.</li></ul><h3>3. Действия с данными</h3><p>Сбор, запись, систематизация, накопление, хранение, уточнение, использование, передача, обезличивание, блокирование, удаление и уничтожение.</p><h3>4. Срок действия</h3><p>С момента предоставления до достижения целей обработки либо до момента отзыва.</p><h3>5. Отзыв</h3><p>Согласие может быть отозвано путём направления письменного обращения на info@vibeturistic.ru.</p>"},
    {"title": "Договор публичной оферты", "slug": "offer", "body": "<p>Настоящая Оферта является официальным предложением Исполнителя в адрес любого физического лица.</p><h3>1. Предмет договора</h3><p>Исполнитель обязуется оказать Заказчику услуги по организации тура, а Заказчик обязуется оплатить эти услуги.</p><h3>2. Стоимость и порядок оплаты</h3><ul><li>стоимость тура указывается на Сайте;</li><li>для брони места вносится предоплата;</li><li>оставшаяся сумма вносится до начала тура.</li></ul><h3>3. Изменение программы</h3><p>Маршрут и график являются ориентировочными и могут быть изменены в связи с погодными условиями или иными обстоятельствами.</p><h3>4. Отмена и возврат</h3><p>Заказчик вправе отказаться от тура. При отмене по вине Исполнителя средства возвращаются в полном объёме.</p><h3>5. Ответственность сторон</h3><p>Исполнитель не несёт ответственности за обстоятельства непреодолимой силы.</p>"},
    {"title": "Пользовательское соглашение", "slug": "terms", "body": "<h3>1. Общие положения</h3><p>Сайт предоставляет информацию о туристических услугах и возможность оставить заявку на бронирование.</p><h3>2. Права и обязанности Пользователя</h3><ul><li>предоставлять достоверную информацию;</li><li>не использовать Сайт для распространения вредоносного ПО;</li><li>соблюдать авторские права.</li></ul><h3>3. Интеллектуальная собственность</h3><p>Все материалы Сайта принадлежат Администрации или используются на законных основаниях.</p><h3>4. Ограничение ответственности</h3><p>Администрация не гарантирует бесперебойную работу Сайта.</p><h3>5. Персональные данные</h3><p>Обработка осуществляется в соответствии с Политикой конфиденциальности.</p><h3>6. Изменение условий</h3><p>Администрация вправе изменять условия Соглашения.</p>"},
]

for ld in legal_data:
    lp = LegalPage(
        title=ld["title"],
        slug=ld["slug"],
        body=ld["body"],
    )
    home.add_child(instance=lp)
    lp.save()

print(f"Created {len(legal_data)} legal pages")

# Set SiteSettings
try:
    settings = TourSiteSettings.objects.get(site=site)
except TourSiteSettings.DoesNotExist:
    settings = TourSiteSettings(site=site)

settings.telegram = "https://t.me/vibeturistic"
settings.vk = "https://vk.com/vibeturistic"
settings.whatsapp = "https://wa.me/79900000000"
settings.save()

print("Updated SiteSettings")
print("Done! Seed data loaded successfully.")
