from django.shortcuts import render, redirect
from typing import Any
from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import (
    get_object_or_404, redirect, render
)
from django.contrib.auth import (
    authenticate as dj_authenticate,
    login as dj_login,
    logout as dj_logout,
)
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse, Http404
from django.core import serializers
import random
import json
from core.models import CustomUser, BankAccount
from core.forms import RegisterForm, LoginForm
# Create your views here.
from core.mixin import HttpResponseMixin


def generation_account():
    """Account is 20 chars"""
    ALL_ACCOUNTS = BankAccount.objects.all()
    new_account = ""
    for _ in range(20):
        new_account += str(random.randint(0, 9))

    if new_account in ALL_ACCOUNTS:
        generation_account()

    return new_account


class RegisterView(FormView):
    template_name = 'registration/sign_up.html'
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = CustomUser.objects.create_user(email, password)
        dj_login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = dj_authenticate(email=email, password=password)
        if user:
            dj_login(self.request, user)
        else:
            form.add_error('__all__', 'Invalid data')
            return super().form_invalid(form)
        return super().form_valid(form)


class LogoutView(View):
    def get(self,  request, *args: Any, **kwargs: Any):
        dj_logout(request)
        return redirect(reverse("login"))


class ProfileView(HttpResponseMixin, View):
    """Get and edit user account and show user cards"""
    template_name: str = 'core/profile.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect(
                reverse("login")
            )

        return self.get_http_response(
            request,
            template_name=self.template_name,
            context={
                'user': user,
                'accounts': BankAccount.objects.filter(owner=user)
            }
        )


class ProfileCardView(View):
    pass


@login_required(login_url=reverse_lazy("login"))
def create_account(request):
    user = request.user
    BankAccount.objects.create(
        owner=user,
        number=generation_account(),
    )
    return redirect(reverse("home"))


@login_required(login_url=reverse_lazy("login"))
def home(request):
    if request.user:
        user = request.user
        return render(request, "home.html",
                      {
                          'accounts': BankAccount.objects.filter(owner=user)
                      }
                      )
    return render(request, "home.html")


class GetUsersView(View):
    def get(self, request):
        data = serializers.serialize('json', CustomUser.objects.all())
        return HttpResponse(
            data, content_type='application/json', status=200
        )

    def post(self, request):
        user_data = json.loads(request.body)
        email = user_data.get('email')
        password = user_data.get('password')
        try:
            user = CustomUser.objects.create_user(email, password)
        except Exception as e:
            return JsonResponse(
                data={
                    'error': e
                }, status=400)
        data = {
            'user_id': user.id,
            'user_email': user.email,
        }
        return JsonResponse(data, status=201)

    def delete(self, request):
        try:
            user = CustomUser.objects.get(id=501)
        except:
            raise Http404
        CustomUser.objects.delete_model(user)
        return JsonResponse(
            data={'message': "DELETE"},
            status=204,
        )


class GetUserView(View):
    def get(self, request, id):
        data = serializers.serialize(
            'json',
            CustomUser.objects.filter(id=id)
        )
        return HttpResponse(
            data, content_type='application/json', status=200
        )

    def delete(self, request, id):
        try:
            user: CustomUser = CustomUser.objects.get(id=id)
        except:
            raise Http404
        user.objects.delete_model()
        return JsonResponse(
            data={'message': "DELETE"},
            status=204,
        )
