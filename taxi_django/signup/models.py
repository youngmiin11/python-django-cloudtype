from django.db import models

class UserInfo(models.Model):
    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    kakaopay_deeplink = models.CharField(max_length=255)
    preferred_conditions = models.CharField(max_length=255, null=True)
    average_review_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    class Meta:
        managed = True
        db_table = 'user'




class Chatroom(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.TextField()
    departure = models.CharField(max_length=255, null=True, blank=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    chat_content = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'chatroom'


class Tip(models.Model):
    tip_id = models.AutoField(primary_key=True)
    tip_content = models.TextField()

    class Meta:
        db_table = 'tip'


class UserChatroomConn(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, db_column='user_id')
    room_id = models.ForeignKey(Chatroom, on_delete=models.CASCADE, db_column='room_id')

    class Meta:
        db_table = 'user_chatroom_conn'
        unique_together = (('user_id', 'room_id'),)


class ChatroomKeyword(models.Model):
    chatroom_id = models.ForeignKey(Chatroom, on_delete=models.CASCADE, db_column='chatroom_id')
    tip_id = models.ForeignKey(Tip, on_delete=models.CASCADE, db_column='tip_id')

    class Meta:
        db_table = 'chatroom_keyword'
        unique_together = (('chatroom_id', 'tip_id'),)


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Chatroom, on_delete=models.CASCADE, db_column='room_id')
    reviewer_id = models.ForeignKey(UserInfo, related_name='reviewer', on_delete=models.CASCADE, db_column='reviewer_id')
    reviewee_id = models.ForeignKey(UserInfo, related_name='reviewee', on_delete=models.CASCADE, db_column='reviewee_id')
    score = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'
        constraints = [
            models.CheckConstraint(check=models.Q(score__gte=0) & models.Q(score__lte=5), name='score_range')
        ]
