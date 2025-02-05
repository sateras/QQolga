from django import forms
from apps.core.models import CustomUser
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    phone = forms.CharField(
        label='Введите номер телефона',
        min_length=10,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Введите пароль',
        min_length=8,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label='Повторите пароль'
    )

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('password_confirm')

        if password != repeat_password:
            raise ValidationError(
                'Пароли не совпадают'
            )

    class Meta:
        model = CustomUser
        fields = ['email']


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(),
        label='Почта/Логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Введите пароль'
    )
