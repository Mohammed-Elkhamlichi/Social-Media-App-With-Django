from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.


def profile(request):
    return render(request, 'accounts/profile.html')


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
