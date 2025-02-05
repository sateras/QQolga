# Generated by Django 4.0.5 on 2025-01-29 19:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('phone', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('category', models.CharField(choices=[('WT', 'Пшеница'), ('BR', 'Ячмень'), ('OT', 'Овёс'), ('CR', 'Кукуруза'), ('RY', 'Рожь'), ('RC', 'Рис'), ('ML', 'Просо'), ('TT', 'Тритикале')], default='WT', max_length=2)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('images', models.ImageField(upload_to='post_images/', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата транзакции')),
                ('status', models.CharField(choices=[('Обрабатывается', 'Processing'), ('Успешно', 'Ok'), ('Неверно', 'Bad'), ('Ожидание превышено', 'Late'), ('Отклонено', 'Rejected')], default='Обрабатывается', max_length=18, verbose_name='Статус')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Сумма перевода')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receiv_transactions', to='core.post')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='send_transactions', to='core.post')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакций',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16, unique=True, verbose_name='Номер карты')),
                ('cvv_code', models.CharField(max_length=3, verbose_name='CVV2')),
                ('expiration_date', models.DateField(default=datetime.datetime(2028, 1, 30, 1, 3, 18, 230979), verbose_name='Дата эксплуатации')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=1000, verbose_name='Остаток')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cards', to='core.post')),
            ],
            options={
                'verbose_name': 'Карта',
                'verbose_name_plural': 'Карты',
            },
        ),
    ]
