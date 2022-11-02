from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name='home'),
    path('create-room/', views.create_room, name='create_room'),
    path('<str:room_id>/detail/', views.room_detail, name='room_detail'),
    path('<str:room_id>/detail-js/', views.room_detail_api, name='room_detail_api'),
    path('<str:room_id>/update/', views.update_room, name='update_room'),
    path('<str:room_id>/delete/', views.delete_room, name='delete_room'),
    path('<int:topic_id>/rooms', views.topic_rooms, name='topic_rooms'),
    path('join-quit-topic/<int:topic_id>/<str:state>/', views.join_quit_topic, name='join_quit_topic'),
    path('join-quit-room/<int:room_id>/<str:state>/', views.join_quit_room, name='join_quit_room'),
    path('delete-message/<int:message_id>/', views.delete_message_api, name='delete_message_api')

]
