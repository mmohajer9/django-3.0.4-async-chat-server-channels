import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import *

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self , event):
        print("connected", event)
        other_username = self.scope["url_route"]["kwargs"]["username"]
        me = self.scope.get("user")
        print(other_username , me)
        thread_obj = await self.get_thread(me , other_username)
        # await self.send({
        #     "type" : "websocket.send",
        #     "text" : "This is Django Channels ! You Are Connected Boy !"
        # })
        print(me , thread_obj.id)
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type" : "websocket.accept"
        })

    async def websocket_receive(self , event):
        #? when a message is received from the websocket
        # print("receive", event)
        front_text = event.get("text" , None)
        
        if front_text:
            loaded_dict_data = json.loads(front_text)
            message = loaded_dict_data.get("message")
            print(message)

            user = self.scope.get("user")
            username = "default"

            if user.is_authenticated:
                username = user.username
                
            myResponse = {
                "message" : message,
                "username" : username
            }

            # new_event = {
            #     "type" : "websocket.send",
            #     "text" : json.dumps(myResponse)
            # }

            #? broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type" : "chat_message",
                    "text" : json.dumps(myResponse)
                }
            )

    async def chat_message(self , event):
        #? sends the actual message
        await self.send({
            "type" : "websocket.send",
            "text" : event["text"]
        })

    async def websocket_disconnect(self , event):
        #? when the socket connects
        print("disconnected" , event)

    @database_sync_to_async
    def get_thread(self , user , other_username):
        return Thread.objects.get_or_new(user , other_username)[0]