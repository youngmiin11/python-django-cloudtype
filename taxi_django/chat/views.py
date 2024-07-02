from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import ChatRoom, User
from .serializers import ChatRoomSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@api_view(['POST'])
def create_room(request):
    data = request.data
    serializer = ChatRoomSerializer(data=data)

    if serializer.is_valid():
        chat_room = serializer.save()
        return Response({
            'room_id': chat_room.room_id, 
            'room_name': chat_room.room_name, 
            'departure': chat_room.departure, 
            'destination': chat_room.destination, 
            'departure_time': chat_room.departure_time,
            'participants': []
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    serializer = ChatRoomSerializer(chat_rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def map_view(request):
    return render(request, 'map.html')

@csrf_exempt
def save_locations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_location = data.get('start_location')
        end_location = data.get('end_location')

        # Parse latitude and longitude
        start_lat, start_lng = map(float, start_location.split(','))
        end_lat, end_lng = map(float, end_location.split(','))

        # 임시 데이터로 ChatRoom 생성
        chat_room = ChatRoom.objects.create(
            room_name="Temporary Room", 
            departure=start_location, 
            destination=end_location, 
            departure_lat=start_lat,
            departure_lng=start_lng,
            destination_lat=end_lat,
            destination_lng=end_lng,
            departure_time="2023-01-01T00:00:00Z",
            participants=[]
        )

        return JsonResponse({'success': True, 'room_id': chat_room.room_id})
    return JsonResponse({'success': False})

@api_view(['GET'])
def get_user_info(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    data = {
        'user_id': user.user_id,
        'name': user.name,
        'kakaopay_deeplink': user.kakaopay_deeplink
    }
    return JsonResponse(data)
