from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


"""
When using Friend class 2 rows will be created for friendship.
So that each member of the friendship can occupy both spots
"""


class Friend(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend")
    roomName = models.CharField(max_length=100, unique=False)

    isUnread = models.BooleanField()

    class Meta:
        unique_together = [['user', 'friend']]


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sender")
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="receiver")

    friend1 = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE,
        related_name="friend1")
    friend2 = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE,
        related_name="friend2")

    dateSent = models.DateTimeField(auto_now_add=True)

    content = models.CharField(max_length=200, unique=False, default="")

    class Meta:
        unique_together = []
