from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import User
import math
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm
from accounts.views import is_user_online
from .serializers import MessageSerializer, RoomSerializer
from accounts.serializers import UserSerializer
import json
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


@login_required(login_url='auth:login_user')
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



# room detail views test js fetch and send data
@login_required(login_url='auth:login_user')
def room_detail_js(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    room_id = int(room_id)
    room = Room.objects.get(pk=room_id)
    if request.method == 'POST':
        req = json.loads(request.body)
        user = request.user
        print('request',req)
        Message.objects.create(room=room, user=user, body=req['body'])
        room.participants.add(user)
        messages = Message.objects.filter(room=room)
        users = User.objects.all()
        participants = room.participants.all()
        # serializers
        roomSerializer = RoomSerializer(room, many=False)
        userSerializer = UserSerializer(user, many=False)
        messagesSerializer = MessageSerializer(messages, many=True)
        usersSerializer = UserSerializer(users, many=True)
        participantsSerializer = UserSerializer(participants, many=True)
        data = {
            "messages": messagesSerializer.data,
            "users": usersSerializer.data,
            "room": roomSerializer.data,
            "room_participants": participantsSerializer.data,
            "authenticate_user": userSerializer.data,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"success":False, "message":"method GET not allowed"}, safe=False)




# join or quit room
@login_required(login_url='auth:login_user')
def join_quit_room(request, room_id, state):
    try:
        room_id = int(room_id)
        room = Room.objects.get(pk=room_id)
        print(room_id, room, state)
        # if the user not participant in the room and he want to join
        if request.user not in room.participants.all() and str(state).lower() == "join":
            room.participants.add(request.user)
            room.save()
            return JsonResponse({"success":"true","message":"user join room success"})
        # else
        elif request.user in room.participants.all() and str(state).lower() == "quit":
            room.participants.remove(request.user)
            room.save()
            return JsonResponse({"success":"true","message":"user quit room success"})
        else:
            return JsonResponse({"success":"false","message":"Internal Server Error"})
    except:
            return JsonResponse({"success":"false","message":"Internal Server Error"})



# create new room
@login_required(login_url='auth:login_user')
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
@login_required(login_url='auth:login_user')
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
        "topics":Topic.objects.all()
    })

# delete room


@login_required(login_url='auth:login_user')
def delete_room(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    try:
        room = Room.objects.get(pk=room_id)
        room.delete()
        return redirect('core:home')
    except Room.DoesNotExist:
        raise Http404

@login_required(login_url='auth:login_user')
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



@login_required(login_url='auth:login_user')
# join or quit topic
def join_quit_topic(request, topic_id, state):
    # join-quit-topic-js/<int:topic_id>/<str:state/
    # add new Joined (join a topic)
        topic_id = int(topic_id)
        print(topic_id, state)
        try:
            # if the topic name exist and the user need to join the topic
            topic = get_object_or_404(Topic,pk=topic_id)
            if str(state).lower() == "join":
                topic.subscribers.add(request.user)
                return JsonResponse({"success":"true","message":"user join topic success"})
            # if the topic name exist and the user need to join the topic
            elif str(state).lower() == "quit":
                topic.subscribers.remove(request.user)
                return JsonResponse({"success":"true","message":"user quit topic success"})
        except:
            return JsonResponse({"success":"false","message":"Internal Server Error"})
