# Generated by Django 4.0.5 on 2025-02-05 12:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_card_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2028, 2, 5, 18, 9, 22, 492813), verbose_name='Дата эксплуатации'),
        ),
    ]
