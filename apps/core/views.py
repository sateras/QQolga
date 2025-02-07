from django.urls import reverse, reverse_lazy
from django.views import View
from django.shortcuts import (
    redirect, render, get_object_or_404
)
from django.contrib.auth import (
    authenticate as dj_authenticate,
    login as dj_login,
    logout as dj_logout,
)
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse, Http404
from django.core import serializers
from typing import Any
from apps.core.models import Post
from apps.auths.forms import RegisterForm, LoginForm, ProfilePictureUpdateForm
from apps.core.mixin import HttpResponseMixin
from apps.auths.models import CustomUser
import random
import json
from .models import Post
from apps.core.forms import PostForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView


class ViewPostListView(ListView):
    model = Post
    template_name = "core/view_posts.html"
    context_object_name = "posts"
    ordering = ['-date_created']


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "core/create_post.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        """Autintificate user (owner)"""
        form.instance.owner = self.request.user
        return super().form_valid(form)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, owner=request.user)
    post.delete()
    return redirect('core:profile')

def generation_account():
    """Account is 20 chars"""
    ALL_ACCOUNTS = Post.objects.all()
    new_account = ""
    for _ in range(20):
        new_account += str(random.randint(0, 9))

    if new_account in ALL_ACCOUNTS:
        generation_account()

    return new_account


class RegisterView(FormView):
    template_name = 'registration/sign_up.html'
    form_class = RegisterForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        number = form.cleaned_data.get('phone')
        password = form.cleaned_data.get('password')
        user = CustomUser.objects.create_user(email, number, password)
        dj_login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("core:home")

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
        return redirect(reverse("core:home"))



class ProfileView(HttpResponseMixin, View):
    """Get and edit user account and show user cards"""
    template_name: str = 'core/profile.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        
        form = ProfilePictureUpdateForm(instance=request.user)

        return self.get_http_response(
            request,
            template_name=self.template_name,
            context={
                'user': request.user,
                'posts': Post.objects.filter(owner=request.user),
                'form': form,
            }
        )

    def post(self, request: WSGIRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        form = ProfilePictureUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("core:profile"))

        return self.get_http_response(
            request,
            template_name=self.template_name,
            context={
                'user': request.user,
                'posts': Post.objects.filter(owner=request.user),
                'form': form,
            }
        )



# @login_required(login_url=reverse_lazy("login"))
def home(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, "home.html",
                      {
                          'posts': Post.objects.filter(owner=user)
                      }
                      )
    return render(request, "home.html", {'posts': []})



class GetUsersView(View):
    def get(self, request):
        data = serializers.serialize('json', CustomUser.objects.all())
        return HttpResponse(
            data, content_type='application/json', status=200
        )

    def post(self, request):
        user_data = json.loads(request.body)
        email = user_data.get('email')
        phone = user_data.get('phone')
        password = user_data.get('password')
        try:
            user = CustomUser.objects.create_user(email, phone, password)
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
