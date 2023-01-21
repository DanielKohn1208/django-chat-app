import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from .models import Friend, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        self.user = self.scope["user"]
        isAuthorized = True

        self.isInRoom = False
        if (self.room_name != "None"):
            self.room_group_name = "chat_%s" % self.room_name
            self.friendrows = await self.get_friendrows()
            self.friend = await self.get_friend()
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            isAuthorized = await self.isAuthorized()
            self.isInRoom = True
        # Authenticate users
        self.notification_group_name = "notif_%s" % self.user.id
        await self.channel_layer.group_add(self.notification_group_name, self.channel_name)
        if isAuthorized:
            await self.accept()

    async def disconnect(self,close_code):
        print("the close code is ",close_code)
        await self.channel_layer.group_discard(
            self.notification_group_name, self.channel_name
        )
        if self.isInRoom:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )


    # needs to be tested not sure if it works
    @database_sync_to_async
    def isAuthorized(self):
        try:
            self.friendrows.get(user=self.user)
            return True
        except ObjectDoesNotExist:
            return False

    @database_sync_to_async
    def get_friendrows(self):
        return Friend.objects.filter(roomName=self.room_name)

    @database_sync_to_async
    def get_friend(self):
        return self.friendrows.get(user=self.user).friend

    @database_sync_to_async
    def save_message(self, content):
        try:
            messageReceiver = self.friend

            friendToChangeStatus = self.friendrows.get(friend=self.user)
            if not friendToChangeStatus.isUnread:

                friendToChangeStatus.isUnread = True
                friendToChangeStatus.save()
            message1 = Message(
                friend1=self.friendrows[0],
                friend2=self.friendrows[1],
                sender=self.user,
                receiver=messageReceiver,
                content=content)
            message2 = Message(
                friend1=self.friendrows[1],
                friend2=self.friendrows[0],
                sender=self.user,
                receiver=messageReceiver,
                content=content)
            message1.save()
            message2.save()
            return True
        except ObjectDoesNotExist:
            return False

    @database_sync_to_async
    def update_read_status(self):
        friendToUpdate = self.friendrows.get(user=self.user)
        friendToUpdate.isUnread = False
        friendToUpdate.save()

    # Receive message from Websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"].strip()
        if len(message) > 0:
            if await self.save_message(message) == False:
                await self.close(3001)
            else:     
                await self.channel_layer.group_send(
                    self.room_group_name, {
                        "type": "chat_message", "message": message, "sender": self.user.username}
                )
                await self.channel_layer.group_send(
                    "notif_%s" % self.friend.id, {
                        "type": "notif_message", "notif_friend_id": self.user.id}
                )
               

    # Receive Notif
    async def notif_message(self, event):
        eventType = event["type"]
        notifFriendId = event["notif_friend_id"]
        print("friend is is ", self.friend.id)
        print("notif id is ", notifFriendId)
        if self.isInRoom:
            if self.friend.id != notifFriendId:
                await self.send(text_data=json.dumps({"event_type": eventType, "notif_friend_id": notifFriendId}))
            else:
                await self.update_read_status()
        else:
            await self.send(text_data=json.dumps({"event_type": eventType, "notif_friend_id": notifFriendId}))

    # Receive Message
    async def chat_message(self, event):
        eventType = event["type"]
        message = event["message"]
        sender = event["sender"]
        await self.send(text_data=json.dumps({"event_type": eventType, "message": message, "sender": sender}))
