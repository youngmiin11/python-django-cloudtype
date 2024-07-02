from rest_framework import serializers
from .models import ChatRoom

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['room_id', 'room_name', 'departure', 'destination', 'departure_time', 'participants', 'created_at']
