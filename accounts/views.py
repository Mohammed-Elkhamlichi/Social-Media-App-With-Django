from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserForm
from accounts.models import User
from django.db.models import Q
from core.models import Room
import online_users.models
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import datetime
# Create your views here.


@login_required(login_url="accounts:login_user")
def profile(request, username):
    rooms = Room.objects.filter(host=request.user)
    # get all the users online
    user_status = online_users.models.OnlineUserActivity.get_user_activities(
        timedelta(seconds=60))
    users = (user for user in user_status)
    is_user_online = False
    for user in users:
        # check if the admin online
        if user.user == request.user:
            is_user_online = True
    user_profile = request.user.profile_pic.url
    return render(request, 'accounts/profile.html', {"user_profile": user_profile, "rooms": rooms, "is_user_online": is_user_online})


@login_required(login_url="accounts:login_user")
def edit_profile(request, username):
    # http://localhost:8000/auth/mohammed/profile/edit
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        profile_pic = request.FILES['profile_pic']
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", user.username)
        form = UserForm(instance=user)
    return render(request, "accounts/edit_profile.html",)


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user.username,
                password=password
            )
            if user is not None:
                login(request, user)
                messages.success(
                    request, f'welcome back,{user.username} you login success to your account')
                return redirect('core:home')
            else:
                messages.error(request, 'enter a valid email and password')
        except:
            messages.error(
                request, 'user with this credentials not exist')
    return render(request, 'accounts/login_user.html')


def register_user(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = User.objects.filter(Q(username=username) | Q(email=email))
        if user.count() == 0:
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.email = user.email.lower()
                user.save()
                login(request, user)
                messages.success(request, 'registration success')
                return redirect('core:home')
            else:
                messages.error(request, 'enter a valid credentials')
        else:
            messages.error(
                request, 'User with this username or email is already exist')

    return render(request, 'accounts/register_user.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'success logout')
    return redirect('core:home')
