import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название организации')),
                ('link', models.CharField(blank=True, max_length=50, null=True, verbose_name='сайт компании')),
            ],
            options={
                'verbose_name': 'компания',
                'verbose_name_plural': 'компании',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='тема сообщения')),
                ('message', models.TextField(verbose_name='введите сообщение')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщении',
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Дата создания')),
                ('scheduled_at', models.DateTimeField(verbose_name='Дата отправки')),
                ('periodicity', models.CharField(choices=[('day', 'Раз в день'), ('week', 'Раз в неделю'), ('month', 'Раз в месяц')], max_length=10)),
                ('last_run', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена')], default='created', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Введите полное имя пользователя', max_length=50, verbose_name='ФИО Пользователя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Введите полное имя клиента', max_length=50, verbose_name='фио клиента')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('comment', models.TextField(verbose_name='комментарий')),
                ('company', models.ForeignKey(help_text='Введите название организации', on_delete=django.db.models.deletion.CASCADE, to='newsletter.company', verbose_name='компания')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
    ]