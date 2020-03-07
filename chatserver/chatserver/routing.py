from django.urls import path , re_path
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter , URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator , OriginValidator

from chat.consumers import ChatConsumer
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)

    #? wrap around the websocket : making sure that what ever host or domain name is doing request ,
    #? it will match the ALLOWED_HOSTS in settings.py -- scope of security - allowed hosts
    "websocket" : AllowedHostsOriginValidator(

        #? scope of users
        AuthMiddlewareStack(
            
            #? similar to urls.py but async version !
            URLRouter(
                [

                ]
            )
        )

    )
})