from django import forms
from .models import Room
# my forms


class RoomForm(forms.ModelForm):
    name = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={
            "placeholder": "enter the room name",
            "class": "rounded placeholder:text-green",
        }))

    class Meta:
        model = Room
        fields = '__all__'
