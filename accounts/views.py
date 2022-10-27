from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
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
import datetime
# Create your views here.


@login_required(login_url="accounts:login_user")
def profile(request, username):
    # get the user object
    get_user = User.objects.get(username=username)
    # get rooms of this user
    rooms = Room.objects.filter(host=get_user)
    # get all the users online
    user_status = online_users.models.OnlineUserActivity.get_user_activities(
        timedelta(seconds=60))
    users = (user for user in user_status)
    is_user_online = False
    for user in users:
        # check if the user is online
        if user.user == get_user:
            is_user_online = True
    hosts = User.objects.all()
    return render(request, 'accounts/profile-new.html', {
        "hosts": hosts, 
        "user": get_user,  
        "rooms": rooms, 
        "topics":Topic.objects.all(),
        "is_user_online": is_user_online
        }
    )
# followers of every single user
def user_followers(request,username):
    user = get_object_or_404(User, username=username)
    followers = user.followers
    return render(request, 'accounts/user_followers.html',{
        "followers":followers,
        "hosts":User.objects.all(),
        "rooms":Room.objects.all(),
        "topics":Topic.objects.all()
    })
    
# following of every single user
def user_following(request,username):
    user = get_object_or_404(User, username=username)
    following = user.following
    return render(request, 'accounts/user_following.html',{
        "following":following,
        "hosts":User.objects.all(),
        "rooms":Room.objects.all(),
        "topics":Topic.objects.all()
    })

def follow_unfollow_user(request, username, state):
    # get the user was clicked on follow him
    user = User.objects.get(username=username)
    if request.user not in user.followers.all() and str(state).lower() == "follow":
        # add  follower  and following
        user.followers.add(request.user)
        request.user.following.add(user)
    elif request.user in user.followers.all() and str(state).lower() == 'unfollow':
        # remove follower and following
        user.followers.remove(request.user)
        request.user.following.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url="accounts:login_user")
def edit_profile(request, username):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)     
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username)
    return render(request, "accounts/edit_profile.html",{
        "rooms":Room.objects.all(),
        "topics":Topic.objects.all(),
        "hosts":User.objects.all()
        }
    )


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
                return redirect('accounts:profile', user.username)
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
    return render(request, 'accounts/register_user.html',{"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, 'success logout')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
