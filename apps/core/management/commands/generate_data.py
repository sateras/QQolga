from datetime import datetime
import random
import names
from core.models import CustomUser
from django.contrib.auth.hashers import make_password

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Custom command for generate data fo filling up database'

    # def __init__(self, *args, **kwargs):
    #     pass

    def _generate_number(self):
        """Generate number"""

        _number_from = 10
        _number_to = 99

        return random.randint(
            _number_from,
            _number_to,
        )

    def _generate_users(self):
        """Generate user/customuser objects"""

        TOTAL_USER_COUNT = 500

        def generate_username():
            return '{0}_{1}'.format(
                first_name.lower(),
                last_name.lower(),
            )

        def generate_email():
            _email_patterns: tuple = (
                'gmail.com', 'mail.ru',
                'yandex.ru', 'mail.ua',
                'inbox.ua', 'yahoo.com',
                'bk.ru'
            )
            return '{0}_{1}@{2}'.format(
                first_name.lower(),
                last_name.lower(),
                random.choice(_email_patterns)
            )

        def generate_password() -> str:
            _password_pattern: str = 'abcde12345'
            _password_max_length: int = 8

            raw_password: str = ''.join(
                random.choice(_password_pattern)
                for _ in range(_password_max_length)
            )
            return make_password(raw_password)

        # Generate superuser
        #
        if not CustomUser.objects.filter(is_superuser=True).exists():
            superuser: dict = {
                'is_staff': True,
                'is_superuser': True,
                'email': 'root@root.ru',
                'password': make_password('qwerty')
            }
            CustomUser.objects.create(**superuser)

        # Generate users
        #
        if CustomUser.objects.filter(
            is_superuser=False
        ).count() >= TOTAL_USER_COUNT:
            return
        # User fields
        username = ''
        first_name = ''
        last_name = ''
        email = ''
        password = ''
        _: int
        for _ in range(TOTAL_USER_COUNT):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            email = generate_email()
            password = generate_password()

            custom_user: dict = {
                'email': email,
                'password': password,
            }
            CustomUser.objects.get_or_create(**custom_user)

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        """Handles data filling"""

        start: datetime = datetime.now()

        self._generate_users()

        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )
