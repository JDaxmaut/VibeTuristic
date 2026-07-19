import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vibe_project.settings.dev")
django.setup()

from django.test import Client
c = Client()
c.login(username='mgr_b9d3d0ee', password='Vibe2025admin')

# Try POST with minimal data
data = {
    'title': 'Test Tour',
    'slug': 'test-tour',
    'is_custom': '',
    'duration_days': 5,
    'duration_label': '5 дней / 4 ночи',
    'group_size': 'до 18',
    'meet_time': '8:30',
    'return_time': 'после 20:00',
    'description': '<p>test</p>',
}
r = c.post('/vibe-admin/pages/3/add/tours/tourpage/', data)
print('status:', r.status_code)
if r.status_code == 200:
    content = r.content.decode(errors='replace')
    # Find error messages
    import re
    errors = re.findall(r'class="error-message"[^>]*>(.*?)</p>', content, re.DOTALL)
    if not errors:
        errors = re.findall(r'<li class="error[^"]*">(.*?)</li>', content, re.DOTALL)
    if not errors:
        errors = re.findall(r'(errorlist.*?</ul>)', content, re.DOTALL)
    if not errors:
        # look for any validation error block
        errors = re.findall(r'(class="help-block[^"]*"[^>]*>(.*?)</span>)', content, re.DOTALL)
    if not errors:
        # find field errors
        errors = re.findall(r'(<ul class="errorlist">(.*?)</ul>)', content, re.DOTALL)
    for e in errors[:10]:
        print('ERROR:', e[0][:200] if isinstance(e, tuple) else e[:200])
    if not errors:
        # look for form-level errors
        level_errors = re.findall(r'alert[^"]*error[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL)
        for e in level_errors[:5]:
            print('LEVEL ERROR:', e[:200])
        if not level_errors:
            print('No errors found in HTML. Checking for hidden messages...')
            msgs = re.findall(r'(class="[^"]*message[^"]*".*?</div>)', content, re.DOTALL)
            for m in msgs[:5]:
                print('MSG:', m[:200])
elif r.status_code == 302:
    print('SUCCESS redirect to:', r.url)
