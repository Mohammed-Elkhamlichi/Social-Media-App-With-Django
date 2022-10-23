from django.urls import path
from core.views import home, room_detail, create_room, update_room, delete_room

app_name = "core"

urlpatterns = [
    path('', home, name='home'),
    path('create-room/', create_room, name='create_room'),
    path('<str:room_id>/detail/', room_detail, name='room_detail'),
    path('<str:room_id>/update/', update_room, name='update_room'),
    path('<str:room_id>/delete/', delete_room, name='delete_room'),

]
