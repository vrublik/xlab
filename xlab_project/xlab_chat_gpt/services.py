import json
from typing import List

from django.conf import settings
from openai import OpenAI, APIStatusError
from openai.types.chat import ChatCompletion
from rest_framework import status
from rest_framework.authtoken.admin import User

from .errors import GenericAPIException
from .models import Message


class MessageGPT:
    def __init__(self, data: dict, user: User, model: str = 'gpt-4o', max_tokens: int = 50, stream: bool = False,
                 api_key: str = settings.OPENAI_API_KEY):
        self.model = model
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=api_key)
        self.data = data
        self.user = user
        self.stream = stream

    def get_response_content(self, response):
        return response.choices[0].message.content

    def create_message(self, save=True) -> Message:
        chat_gpt_message = self.set_chat_gpt_messages(self.data)
        chat_gpt_response = self.get_response_chat_gpt(chat_gpt_message)
        try:
            message = Message(
                user=self.user,
                request=self.data['message'],
                assistant_content=self.data.get('assistant_content'),
                response=self.get_response_content(chat_gpt_response)
            )
        except ValueError as e:
            raise GenericAPIException(default_detail='Anonymous user, please login.',
                                      status_code=status.HTTP_401_UNAUTHORIZED)

        if save:
            message.save()

        return message

    @staticmethod
    def set_chat_gpt_messages(data: dict) -> List[dict]:
        user_message = data.get('message')
        assistant_content = data.get('assistant_content')

        messages = [
            {'role': 'user', 'content': user_message}
        ]

        if assistant_content:
            messages.append({'role': 'assistant', 'content': assistant_content})

        return messages

    def get_response_chat_gpt(self, messages: List[dict]) -> ChatCompletion:
        try:
            response = self.client.chat.completions.create(messages=messages, model=self.model,
                                                           max_tokens=self.max_tokens, stream=self.stream)
        except APIStatusError as e:
            raise GenericAPIException(default_detail=json.loads(e.response.text), status_code=e.status_code)

        return response


class AsyncMessageGPT(MessageGPT):
    CHUNK_RESPONSE_SIZE = 30

    def __init__(self, send_json, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.send_json = send_json

    async def get_response_content(self, response):
        full_response = ''
        chunk_response = ''
        for chunk in response:
            if chunk.choices[0].delta.content:
                chunk_response += chunk.choices[0].delta.content
                if len(chunk_response) > self.CHUNK_RESPONSE_SIZE:
                    await self.send_json(content=json.dumps({'message': chunk_response}))
                    full_response += chunk_response
                    chunk_response = ''
        if chunk_response:
            await self.send_json(content=json.dumps({'message': chunk_response}))
            full_response += chunk_response

        return full_response

    async def create_message(self, save=True) -> Message:
        chat_gpt_message = self.set_chat_gpt_messages(self.data)
        chat_gpt_response = self.get_response_chat_gpt(chat_gpt_message)
        response = await self.get_response_content(chat_gpt_response)

        try:
            message = Message(
                user=self.user,
                request=self.data['message'],
                assistant_content=self.data.get('assistant_content'),
                response=response
            )
        except ValueError as e:
            raise GenericAPIException(default_detail='Anonymous user, please login.',
                                      status_code=status.HTTP_401_UNAUTHORIZED)

        if save:
            await message.asave()

        return message
