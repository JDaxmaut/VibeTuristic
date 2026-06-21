from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0009_home_included_seed'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingLead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('contact', models.CharField(max_length=100, verbose_name='Контакт (тел./TG)')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('tour_name', models.CharField(blank=True, max_length=200, verbose_name='Тур')),
                ('departure_label', models.CharField(blank=True, max_length=200, verbose_name='Заезд')),
                ('msg', models.TextField(blank=True, verbose_name='Сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ['-created_at'],
            },
        ),
    ]
