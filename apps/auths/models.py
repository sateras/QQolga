from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Q, QuerySet

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, phone: str, password: str) -> 'CustomUser':
        if not email:
            raise ValidationError('Email required')

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            phone=phone,
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
        


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        'Имя',
        max_length=50
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=50
    )
    email = models.EmailField(
        'Почта/Логин',
        unique=True,
    )
    number = models.CharField(
        'Номер телефона',
        max_length=11,
    )
    is_active: models.BooleanField(
        'Активность',
        default=True,
    )
    is_staff = models.BooleanField(
        'Статус менеджера',
        default=False,
    )

    data_joined = models.DateTimeField(
        'Время создания',
        default=timezone.now,
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
