from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home1'),
    path('sign_up/', views.RegisterView.as_view(), name='sign_up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('api/users/', views.GetUsersView.as_view()),
    path('api/users/<int:id>', views.GetUserView.as_view()),
    path('create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('view_posts/', views.ViewPostListView.as_view(), name='view_post'),

]
