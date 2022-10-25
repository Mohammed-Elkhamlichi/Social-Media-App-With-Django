from django import forms
from .models import Room, Message
# my forms


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('host', 'name', 'topic', 'description')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['user', 'room', 'body', ]
