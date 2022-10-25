from django import forms
from .models import Room
# my forms


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('host', 'name', 'topic', 'description')
