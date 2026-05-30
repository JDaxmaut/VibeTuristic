<div align="center">

# 🏔️ Vibe Turistic

**Молодёжные туры по Дагестану — горы, каньоны, водопады и барханы.**

[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Wagtail](https://img.shields.io/badge/Wagtail-CMS-43B1B0?style=flat-square&logo=wagtail&logoColor=white)](https://wagtail.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)

</div>

---

## ✨ Возможности

- 🗓️ **Расписание заездов** — по каждому туру с датами, статусом мест (есть / мало / нет)
- 📸 **Фотогалерея** — добавляется через Wagtail-админку, хранится как инлайн к туру
- 📋 **Управление контентом** — все тексты, цены, чек-листы и фото редактируются в админке
- 📱 **Адаптивная навигация** — sticky top-bar на десктопе, fixed bottom-bar на мобильных (скрывается при скролле вниз)
- 📄 **Юридические страницы** — с боковым меню и навигацией между документами
- 📬 **Форма бронирования** — динамический выбор дат по выбранному туру через JS

---

## 🛠️ Стек

| Слой | Технология |
|---|---|
| Backend | Django 6.0 + Wagtail CMS |
| База данных | SQLite (dev) |
| Шаблоны | Django Templates |
| Стили | Кастомный CSS (дизайн-система Vibe) |
| Деплой | Docker + Gunicorn |

---

## 🚀 Быстрый старт

### Локально

```bash
# 1. Клонировать репозиторий
git clone https://github.com/JDaxmaut/VibeTuristic.git
cd VibeTuristic/vibe_project

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Применить миграции
python manage.py migrate

# 4. Создать суперпользователя для админки
python manage.py createsuperuser

# 5. Заполнить базу тестовыми данными
cd ..
python seed_db.py

# 6. Запустить сервер
cd vibe_project
python manage.py runserver
```

Сайт: [http://localhost:8000](http://localhost:8000)
Админка: [http://localhost:8000/admin](http://localhost:8000/admin)

### Docker

```bash
cd vibe_project
docker build -t vibeturistic .
docker run -p 8000:8000 vibeturistic
```

---

## 📁 Структура проекта

```
VibeTuristic/
├── vibe_project/           # Django-проект
│   ├── home/               # Приложение главной страницы
│   ├── tours/              # Туры, заезды, отзывы, настройки
│   │   ├── models.py       # TourPage, Departure, Review, Gallery...
│   │   ├── templates/      # Шаблоны страниц
│   │   └── migrations/     # Миграции БД
│   └── vibe_project/
│       ├── static/
│       │   ├── css/vibe.css    # Дизайн-система
│       │   └── js/site.js      # Интерактивность
│       └── templates/base.html
├── seed_db.py              # Скрипт начального заполнения БД
├── docs/                   # Юридические документы (HTML-прототипы)
├── stock-photos/           # Стоковые фото для туров
└── assets/                 # Спрайт иконок SVG
```

---

## ⚙️ Управление контентом

Весь контент редактируется через Wagtail-админку (`/admin`):

- **Туры** → Pages → редактировать `TourPage`
- **Заезды** → Snippets → Заезды
- **Отзывы** → Snippets → Отзывы
- **Настройки** → Settings → Настройки сайта (телефон, соцсети)
- **Фотогалерея** → внутри каждого тура, вкладка «Фотогалерея»

---

## 🌍 Деплой

Проект готов к деплою через Docker. При сборке контейнер автоматически:
1. Устанавливает зависимости
2. Собирает статику (`collectstatic`)
3. Применяет миграции
4. Запускает `gunicorn`

Для production необходимо задать переменные окружения:
```env
DJANGO_SETTINGS_MODULE=vibe_project.settings.production
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
```

---

<div align="center">

Сделано с вайбом 🐑 в Дагестане

</div>
