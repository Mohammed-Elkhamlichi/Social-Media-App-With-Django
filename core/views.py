from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Room
from django.contrib.auth.decorators import login_required
from .forms import RoomForm
# Create your views here.

#


@login_required(login_url='auth:login_user')
def home(request):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    rooms = Room.objects.all()
    return render(request, 'core/home.html', {"title": 'Room Page', 'rooms': rooms},)


@login_required(login_url='auth:login')
def room_detail(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    room_id = int(room_id)
    room = Room.objects.get(pk=room_id)
    return render(request, 'core/room_detail.html', {"title": 'Room Detail Page', 'room': room})


@login_required(login_url='auth:login')
def create_room(request):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')

    return render(request, 'core/room_form.html', {"form": form, "is_update": True, "method": "POST"})


@login_required(login_url='auth:login')
def update_room(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    room = Room.objects.get(pk=room_id)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('core:home')

    return render(request, 'core/room_form.html', {"form": form, "is_update": True, "method": "PUT"})


@login_required(login_url='auth:login')
def delete_room(request, room_id):
    if not request.user.is_authenticated:
        redirect('auth:login_user')
    try:
        room = Room.objects.get(pk=room_id)

        room.delete()
        return redirect('core:home')
    except Room.DoesNotExist:
        raise Http404
