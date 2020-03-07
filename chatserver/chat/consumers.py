import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import *

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self , event):
        print("connected", event)
        await self.send({
            "type" : "websocket.accept"
        })
        other_username = self.scope["url_route"]["kwargs"]["username"]
        me = self.scope.get("user")
        print(other_username , me)
        thread_obj = await self.get_thread(me , other_username)
        await self.send({
            "type" : "websocket.send",
            "text" : "Hellooooo This is Django Channels"
        })

    async def websocket_receive(self , event):
        #? when a message is received from the websocket
        # print("receive", event)
        front_text = event.get("text" , None)
        
        if front_text:
            loaded_dict_data = json.loads(front_text)
            message = loaded_dict_data.get("message")
            print(message)
            await self.send({
                "type" : "websocket.send",
                "text" : message
            })
    async def websocket_disconnect(self , event):
        #? when the socket connects
        print("disconnected" , event)

    @database_sync_to_async
    def get_thread(self , user , other_username):
        return Thread.objects.get_or_new(user , other_username)[0]