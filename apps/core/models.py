from django.db import models
from datetime import datetime, timedelta
from apps.auths.models import CustomUser


class Post(models.Model):

    class Category(models.TextChoices):
        WHEAT = 'WT', 'Пшеница'
        BARLEY = 'BR', 'Ячмень'
        OATS = 'OT', 'Овёс'
        CORN = 'CR', 'Кукуруза'
        RYE = 'RY', 'Рожь'
        RICE = 'RC', 'Рис'
        MILLET = 'ML', 'Просо'
        TRITICALE = 'TT', 'Тритикале'

    owner: CustomUser = models.ForeignKey(
        CustomUser, related_name='posts', on_delete=models.PROTECT,
    )
    title: str = models.CharField(
        verbose_name="Заголовок", max_length=100
    )
    text: str = models.TextField(
        verbose_name="Текст"
    )
    phone: str = models.CharField(
        verbose_name="Номер телефона", max_length=15
    )
    category: str = models.CharField(
        max_length=2, choices=Category.choices, default=Category.WHEAT
    )
    date_created: str = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True
    )
    images: str = models.ImageField(
        verbose_name="Изображение", upload_to="post_images/"
    )
    price: str = models.DecimalField(
        verbose_name="Цена", max_digits=10, decimal_places=2
    )

    def __str__(self) -> str:
        return f'{self.title} - {self.get_category_display()}'



