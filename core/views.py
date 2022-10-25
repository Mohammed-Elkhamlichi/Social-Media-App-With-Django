from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotAllowed
from .models import Room, Topic
from django.contrib.auth.decorators import login_required
from .forms import RoomForm
from django.db.models import Q
from accounts.models import User
import math
from django.contrib import messages
# Create your views here.


@login_required(login_url='auth:login_user')
def home(request):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    hosts = User.objects.all().order_by('username')
    limit_display_rooms = 10
    rooms = Room.objects.all()[:limit_display_rooms]

    # add new Joined (join a topic)
    if request.method == 'POST':
        joined_topic_name = request.POST.get('joined_topic')
        quit_join = request.POST.get('quit_join')
        # if the topic name exist and the user need to join the topic
        try:
            if joined_topic_name is not None and quit_join == "Join":
                joined_topic = Topic.objects.get(name=joined_topic_name)
                joined_topic.users.add(request.user)
                messages.success(request, f'you joined the Topic successfully')
        except:
            messages.success(request, f'Internal Server Error')

        # if the topic name exist and the user need to join the topic
        try:
            if joined_topic_name is not None and quit_join == "Quit":
                joined_topic = Topic.objects.get(name=joined_topic_name)
                joined_topic.users.remove(request.user)
                messages.success(request, f'you quit the Topic successfully')
        except:
            messages.success(request, f'Internal Server Error')

    topics = Topic.objects.all().order_by('name')

    # pagination
    page_number = request.GET.get('page')
    if page_number is not None:
        x = int(page_number)*limit_display_rooms
        rooms = Room.objects.all()[(x-limit_display_rooms):x]
    pages = math.floor(Room.objects.count() / limit_display_rooms)

    # search for rooms
    search = request.GET.get('search')
    if search is not None:
        rooms = Room.objects.filter(
            Q(name__contains=search)
        ).order_by('-created', '-updated')
    context = {
        "title": 'Room Page',
        'rooms': rooms,
        "range": range(1, pages+1),
        "topics": topics,
        "hosts": hosts,
    }
    return render(request, 'core/home.html', context)


@ login_required(login_url='auth:login')
def room_detail(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    room_id = int(room_id)
    room = Room.objects.get(pk=room_id)
    return render(request, 'core/room_detail.html', {"title": 'Room Detail Page', 'room': room})


@ login_required(login_url='auth:login')
def create_room(request):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    form = RoomForm()
    if request.method == 'POST':
        host = request.POST.get('id_host')
        participant = request.POST.get('id_participants')
        topic = Topic.objects.filter(name=request.POST.get('id_topic')).first()
        if topic is None:
            # create new topic
            topic = Topic.objects.create(name=request.POST.get('id_topic'))
            topic = topic.users.add(request.user)
            return topic
        description = request.POST.get('description')
        name = request.POST.get('name')
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.topic = topic
            room.participants.add(request.user.username.id)
            room.description = description
            room.name = name
            room.save()
            # room.participants_set.create(participant)
            messages.success(request, 'room has been created')
            return redirect("core:home")
        else:
            messages.error(request, 'Form not valid')
            return redirect("core:create_room")

    else:
        form = RoomForm()
    context = {
        "form": form,
        "is_update": False,
        "method": "POST",
        'topics': Topic.objects.all()
    }
    return render(request, 'core/room_form.html', context)


@ login_required(login_url='auth:login')
def update_room(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    room = Room.objects.get(pk=room_id)
    form = RoomForm(instance=room)
    if request.method == "POST":
        topic = Topic.objects.filter(name=request.POST.get('id_topic')).first()
        if topic is None:
            # create new topic
            topic = Topic.objects.create(name=request.POST.get('id_topic'))
            topic = topic.users.add(request.user)
            return topic
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form = form.save(commit=False)
            form.host = request.user
            form.topic = topic
            form.save()
            return redirect('core:home')
    else:
        form = RoomForm()
    context = {
        "form": form,
        "room": room,
        "is_update": True,
        "method": "PUT"
    }
    return render(request, 'core/room_form.html', context)


@ login_required(login_url='auth:login')
def delete_room(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    try:
        room = Room.objects.get(pk=room_id)

        room.delete()
        return redirect('core:home')
    except Room.DoesNotExist:
        raise Http404
