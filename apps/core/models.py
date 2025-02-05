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



class Transactions(models.Model):

    class StatusTransactions(models.TextChoices):
        PROCESSING = 'Обрабатывается'
        OK = 'Успешно'
        BAD = 'Неверно'
        LATE = 'Ожидание превышено'
        REJECTED = 'Отклонено'

    sender: Post = models.ForeignKey(
        Post, related_name="send_transactions", on_delete=models.PROTECT
    )
    receiver: Post = models.ForeignKey(
        Post, related_name="receiv_transactions", on_delete=models.PROTECT
    )
    date = models.DateTimeField(
        verbose_name='Дата транзакции',
        auto_now_add=True,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=18,
        choices=StatusTransactions.choices,
        default=StatusTransactions.PROCESSING
    )
    amount = models.DecimalField(
        verbose_name='Сумма перевода',
        decimal_places=2,
        max_digits=8
    )

    def __str__(self) -> str:
        return f'{self.sender}->{self.receiver}:{self.amount}'

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакций"


class Card(models.Model):
    account = models.ForeignKey(
        Post, related_name='cards', on_delete=models.PROTECT,
    )
    number = models.CharField(
        verbose_name="Номер карты",
        max_length=16,
        unique=True,
    )
    cvv_code = models.CharField(
        verbose_name="CVV2", max_length=3,
    )
    expiration_date = models.DateField(
        verbose_name='Дата эксплуатации',
        default=(datetime.now()+timedelta(365*3)),
    )
    balance = models.DecimalField(
        verbose_name='Остаток',
        default=0,
        decimal_places=2,
        max_digits=1000,
    )

    def __str__(self) -> str:
        return self.number

    class Meta:
        verbose_name = "Карта"
        verbose_name_plural = "Карты"
