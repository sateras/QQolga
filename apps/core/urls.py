from django.urls import path
from apps.core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('sign_up/', views.RegisterView.as_view(), name='sign_up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create_account/', views.create_account, name='create_account'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/card', views.ProfileCardView.as_view(), name='profile_card'),
    path('api/users/', views.GetUsersView.as_view()),
    path('api/users/<int:id>', views.GetUserView.as_view()),
]