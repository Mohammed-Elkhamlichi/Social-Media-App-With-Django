
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserForm
from accounts.models import User
from django.db.models import Q
from core.models import Room, Topic
import online_users.models
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
import datetime
import json
# Create your views here.

# check if the user online or not


def is_user_online(username):
    # get the user object
    get_user = User.objects.get(username=username)
    # get all the users online
    user_status = online_users.models.OnlineUserActivity.get_user_activities(
        timedelta(seconds=60))
    users = (user for user in user_status)
    for user in users:
        # check if the user is online
        if user.user == get_user:
            return True


@login_required(login_url="accounts:login_user")
def profile(request, username):
    # get the user object
    get_user = User.objects.get(username=username)
    # get rooms of this user
    rooms = Room.objects.filter(host=get_user)
    # is_user_online(username)
    hosts = User.objects.all()
    return render(request, 'accounts/profile.html', {
            "hosts": hosts,
            "user": get_user,
            "rooms": rooms,
            "topics": Topic.objects.all(),
            "is_user_online": is_user_online(username)
        })
    
@login_required(login_url="accounts:login_user")
# followers of every single user
def user_followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()
    return render(request, 'accounts/user_followers.html', {
        "followers": followers,
        "hosts": User.objects.all(),
        "rooms": Room.objects.all(),
        "topics": Topic.objects.all(),
        "is_user_online": is_user_online(username)
    })


@login_required(login_url="accounts:login_user")
# following of every single user
def user_following(request, username):
    user = get_object_or_404(User, username=username)
    following = user.following.all()
    return render(request, 'accounts/user_following.html', {
        "following": following,
        "hosts": User.objects.all(),
        "rooms": Room.objects.all(),
        "topics": Topic.objects.all(),
        "is_user_online": is_user_online(username)
    })


@login_required(login_url="accounts:login_user")
# 
def follow_unfollow_user(request, username, state):
    # get the user was clicked on follow him
    username = str(username)
    user = User.objects.get(username=username)
    print('state',state,'username',username)
    if request.user not in user.followers.all() and str(state).lower() == "follow":
        # add  follower  and following
        user.followers.add(request.user)
        request.user.following.add(user)
        return JsonResponse({"success":True})
    elif request.user in user.followers.all() and str(state).lower() == 'unfollow':
        # remove follower and following
        user.followers.remove(request.user)
        request.user.following.remove(user)
        return JsonResponse({"success":True})
    else:
        return  JsonResponse({"success":False})
    return  JsonResponse({"success":False})


@login_required(login_url="accounts:login_user")
def edit_profile(request, username):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username)
    return render(request, "accounts/edit_profile.html", {
        "rooms": Room.objects.all(),
        "topics": Topic.objects.all(),
        "hosts": User.objects.all(),
        "is_user_online": is_user_online(username)
    })

def login_user(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    return render(request, 'accounts/login_user.html')


def login_user_api(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user.username,
                password=password
            )
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success':True, 
                    "message":'Login Success', 
                    "username":user.username
                    })
            else:
                return JsonResponse({"success":False, "message":"Incorrect Email or Password "})
        except:
            return JsonResponse({"success":False, "message":"User not exist"})


def register_user(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form)
        username = str(request.POST.get('username'))
        email = str(request.POST.get('email'))
        user = User.objects.filter(Q(username=username) | Q(email=email))
        if user.count() == 0 and form.is_valid():
            user = form.save(commit=False)
            user.username = username.lower()
            user.email = email.lower()
            user.save()
            login(request, user)
            return redirect('core:home')
    return render(request, 'accounts/register_user.html', {"form": form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login_user'))
