from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import User
import math
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm
from accounts.views import is_user_online
# Create your views here.


@login_required(login_url='auth:login_user')
def home(request):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    hosts = User.objects.all().order_by('-username')
    limit_display_rooms = 10
    rooms = Room.objects.all()[:limit_display_rooms]
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
            Q(name__icontains=search)
        ).order_by('-created', '-updated')
    context = {
        "title": 'Room Page',
        'rooms': rooms,
        "range": range(1, pages+1),
        "topics": topics,
        "hosts": hosts,
    }
    return render(request, 'core/home.html', context=context)

# room detail


@ login_required(login_url='auth:login')
def room_detail(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    room_id = int(room_id)
    room = Room.objects.get(pk=room_id)
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        print(form)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.room = room
            form.save()
            room.participants.add(request.user)
            form = MessageForm()
            return redirect(request.META.get('HTTP_REFERER', '/'))
            # return redirect('core:room_detail', room.id)
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = MessageForm()
    conversation = Message.objects.filter(room=room)
    context = {
        "title": 'Room Detail Page',
        'room': room,
        "rooms": Room.objects.all(),
        "topics": Topic.objects.all(),
        "hosts": User.objects.all(),
        "conversation": conversation,
    }
    return render(request, 'core/room_detail.html', context=context)


# join or quit room
def join_quit_room(request, room_id, state):
    room_id = int(room_id)
    room = Room.objects.get(pk=room_id)
    # if the user not participant in the room and he want to join
    if request.user not in room.participants.all() and str(state).lower() == "join":
        room.participants.add(request.user)
        room.save()
    # else
    elif request.user in room.participants.all() and str(state).lower() == "quit":
        room.participants.remove(request.user)
        room.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


# create new room
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
            topic = topic.subscribers.add(request.user)
            return topic
        description = request.POST.get('description')
        name = request.POST.get('name')
        user = User.objects.get(username=request.user.username)
        form = RoomForm(request.POST)
        if not form.is_valid():
            return redirect(request.META.get('HTTP_REFERER', '/'))
        form = form.save(commit=False)
        form.host = request.user
        form.topic = topic
        form.description = description
        form.name = name
        form.save()
        form.participants.add(request.user)
        form = MessageForm()
        return HttpResponseRedirect('/')

    return render(request, 'core/room_form.html', context={
        "form": form,
        "is_update": False,
        "method": "POST",
        'topics': Topic.objects.all(),
        'hosts': User.objects.all(),
    })


# update room
@ login_required(login_url='auth:login')
def update_room(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    room_id = int(room_id)
    room = Room.objects.get(pk=room_id)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        topic = Topic.objects.filter(name=request.POST.get('id_topic')).first()
        if topic is None:
            # create new topic
            topic = Topic.objects.create(name=request.POST.get('id_topic'))
            topic = topic.subscribers.add(request.user)
            return topic
        # topic = Topic.objects.filter(name=request.POST.get('id_topic')).first()
        form = RoomForm(request.POST or None, instance=room)
        if form.is_valid():
            form = form.save(commit=False)
            form.host = request.user
            form.topic = topic
            form.save()
            return redirect('core:home')

    return render(request, 'core/room_form.html', context={
        "form": form,
        "room": room,
        "is_update": True,
        "method": "PUT",
        "hosts": User.objects.all(),
    })

# delete room


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


# get all room exist in every single topic
def topic_rooms(request, topic_id):
    topic_id = int(topic_id)
    topic = get_object_or_404(Topic, pk=topic_id)
    rooms = Room.objects.filter(topic=topic)

    return render(request, 'core/topic_rooms.html', {
        "rooms": rooms,
        "topics": Topic.objects.all(),
        "hosts": User.objects.all(),
    })


# join or quit topic
def join_quit_topic(request):
    # add new Joined (join a topic)
    if request.method == 'POST':
        topic_name = request.POST.get('joined_topic')
        quit_topic = request.POST.get('quit_topic')
        join_topic = request.POST.get('join_topic')
        print(join_topic, quit_topic, topic_name)
        try:
            # if the topic name exist and the user need to join the topic
            joined_topic = Topic.objects.get(name=topic_name)
            if topic_name is not None and str(join_topic).lower() == "join":
                joined_topic.subscribers.add(request.user)

            # if the topic name exist and the user need to join the topic
            elif topic_name is not None and str(quit_topic).lower() == "quit":
                joined_topic.subscribers.remove(request.user)
        except:
            messages.success(request, f'Internal Server Error')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
