import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from .models import Room, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        # Send welcome message
        self.send(
            text_data=json.dumps(
                {
                    "type": "system",
                    "message": f"Welcome to {self.room_name}!",
                    "user": "System",
                    "timestamp": str(datetime.now()),
                }
            )
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = self.user.username

        # Save message to database
        room = Room.objects.get(slug=self.room_name)
        Message.objects.create(room=room, user=self.user, content=message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": username,
                "timestamp": str(datetime.now()),
            },
        )

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "type": "message",
                    "message": event["message"],
                    "user": event["user"],
                    "timestamp": event["timestamp"],
                }
            )
        )
