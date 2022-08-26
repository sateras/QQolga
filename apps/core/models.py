from operator import mod
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.db.models import Q, QuerySet

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str) -> 'CustomUser':
        if not email:
            raise ValidationError('Email required')

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str) -> 'CustomUser':
        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_special_user(self) -> QuerySet['CustomUser']:
        """Get special users after 2022.07.01"""
        DATE = datetime.date(2022, 7, 1)
        users: QuerySet[CustomUser] = self.filter(
            Q(is_staff=True) & Q(date_joined__gte=DATE)
        )
        return users

    def get_undeleted_users(self) -> QuerySet['CustomUser']:
        """Get undeleted users"""
        users: QuerySet[CustomUser] = self.filter(is_active=True)
        return users

    def delete_model(self):
        self.is_active = False
        self.save()
        return 'Deleted'
        


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'Почта/Логин',
        unique=True
    )
    number = models.CharField(
        'Номер телефона',
        max_length=11,
    )
    is_active: models.BooleanField(
        'Активность',
        default=True
    )
    is_staff = models.BooleanField(
        'Статус менеджера',
        default=False
    )

    data_joined = models.DateTimeField(
        'Время создания',
        default=timezone.now
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = (
            'data_joined',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class BankAccount(models.Model):
    owner = models.ForeignKey(
        CustomUser, related_name='Владелец', on_delete=models.PROTECT,
    )
    number = models.CharField(
        verbose_name="Номер счета",
        max_length=20,
        unique=True,
        null=False,
    )
    date = models.DateTimeField(
        verbose_name='Дата открытия',
        auto_now_add=True,
    )
    balance = models.FloatField(
        verbose_name='Остаток',
        default=0,
    )

    def __str__(self) -> str:
        return f'{self.number}'

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"


class Transactions(models.Model):

    class StatusTransactions(models.TextChoices):
        PROCESSING = 'Обрабатывается'
        OK = 'Успешно'
        BAD = 'Неверно'
        LATE = 'Ожидание превышено'
        REJECTED = 'Отклонено'

    sender = models.ForeignKey(
        BankAccount, related_name="send_transactions", on_delete=models.PROTECT
    )
    receiver = models.ForeignKey(
        BankAccount, related_name="receiv_transactions", on_delete=models.PROTECT
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
        BankAccount, related_name='cards', on_delete=models.PROTECT,
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
