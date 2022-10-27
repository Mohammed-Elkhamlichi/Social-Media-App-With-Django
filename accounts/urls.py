from django.urls import path

from . import views
app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('<str:username>/profile/', views.profile, name='profile'),
    path('<str:username>/profile/edit', views.edit_profile, name='edit_profile'),
    path('<str:username>/follower/', views.set_followers, name='set_followers'),
    path('<str:username>/followers/', views.user_followers, name='user_followers'),
]
