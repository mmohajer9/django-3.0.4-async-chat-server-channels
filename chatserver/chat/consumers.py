import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import *

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self , event):
        print("connected", event)

    async def websocket_receive(self , event):
        #? when a message is received from the websocket
        print("receive", event)

    async def websocket_disconnect(self , event):
        #? when the socket connects
        print("disconnected" , event)