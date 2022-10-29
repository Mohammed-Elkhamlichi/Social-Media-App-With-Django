from rest_framework import serializers
from .models import Message, Room
from accounts.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields ='__all__'
        
class RoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = '__all__'