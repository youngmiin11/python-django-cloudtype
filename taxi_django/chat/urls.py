from django.urls import path
from .views import create_room, get_chat_rooms, map_view, save_locations, get_user_info

urlpatterns = [
    path('create_room/', create_room, name='create_room'),
    path('get_chat_rooms/', get_chat_rooms, name='get_chat_rooms'),
    path('map/', map_view, name='map_view'),
    path('save_locations/', save_locations, name='save_locations'),
    path('user_info/<str:user_id>/', get_user_info, name='get_user_info'),
]
