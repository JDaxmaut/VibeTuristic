import django
import os
import sys

sys.path.insert(0, r"C:\Users\dxmta\Desktop\vige\vibe_project")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vibe_project.settings.dev")

django.setup()

from django.db import connection
from wagtail.models import Page, Site
from django.contrib.contenttypes.models import ContentType
from tours.models import HomePage

homepage_ct = ContentType.objects.get_for_model(HomePage)

# Get the existing page record
wp = Page.objects.get(slug='home')

# Update content type
with connection.cursor() as cursor:
    cursor.execute(
        "UPDATE wagtailcore_page SET content_type_id = %s WHERE id = %s",
        [homepage_ct.id, wp.id]
    )

# Check if a tours_homepage row exists
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM tours_homepage WHERE page_ptr_id = %s", [wp.id])
    exists = cursor.fetchone()[0]

if not exists:
    # We need to create the subclass record. Let's use raw SQL to avoid FK issues
    # First, check the table structure
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(tours_homepage)")
        columns = cursor.fetchall()
        col_names = [c[1] for c in columns]
        print(f"tours_homepage columns: {col_names}")

    # Create the HomePage record
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO tours_homepage (page_ptr_id, hero_headline, hero_ribbon, hero_subtitle, hero_bg_id) "
            "VALUES (%s, %s, %s, %s, NULL)",
            [wp.id, 'Vibe Turistic', '№1 молодёжные туры по Дагестану', 'Горы, каньоны, водопады и барханы — без скучных автобусов. Только вайб, движ и виды, от которых захватывает дух.']
        )
        print("Created tours_homepage record")

# Now refresh and use the HomePage
home = HomePage.objects.get(pk=wp.id)
home.hero_headline = 'Vibe Turistic'
home.hero_ribbon = '№1 молодёжные туры по Дагестану'
home.hero_subtitle = 'Горы, каньоны, водопады и барханы — без скучных автобусов. Только вайб, движ и виды, от которых захватывает дух.'
home.save()
print(f"HomePage ready: {home.title} (pk={home.pk})")

# Update site root
site = Site.objects.get(is_default_site=True)
site.root_page = home
site.save()
print("Site root page updated")

print("Done!")
