from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

from .errors import GenericAPIException
from .serializers import MessageSerializer
from .services import MessageGPT


class ChatConsumer(AsyncJsonWebsocketConsumer):

    @staticmethod
    @database_sync_to_async
    def get_user(token_string):
        try:
            user = Token.objects.get(key=token_string).user
        except ObjectDoesNotExist as e:
            user = None
        return user

    def parse_token(self):
        token = (dict((x.split('=') for x in self.scope['query_string'].decode().split('&')))).get('token', None)
        return token

    async def connect(self):
        try:
            token_key = self.parse_token()
        except ValueError as e:
            await self.close()

        user = await self.get_user(token_key)

        if user:
            self.scope['user'] = user
            await self.accept()
        else:
            await self.close()

    async def receive_json(self, content, **kwargs):
        try:
            message_gpt = MessageGPT(data=content, user=self.scope['user'])
            message = message_gpt.create_message(save=False)
            await message.asave()

            serializer = MessageSerializer(message)
            await self.send_json(content=serializer.data)

        except GenericAPIException as e:
            await self.send_json({
                'type': 'websocket.close',
                'code': e.status_code,
                'reason': e.default_detail
            })


