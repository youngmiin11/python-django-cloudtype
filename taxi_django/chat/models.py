from django.db import models
import uuid

class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    kakaopay_deeplink = models.CharField(max_length=255)
    preferred_conditions = models.CharField(max_length=255, null=True, blank=True)
    average_review_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

class ChatRoom(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    room_name = models.CharField(max_length=100, default='default_room_name')
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.JSONField()
    departure = models.CharField(max_length=255, default='default_departure')
    destination = models.CharField(max_length=255, default='default_destination')
    departure_time = models.DateTimeField(null=True, blank=True)
    chat_content = models.TextField(null=True, blank=True)
