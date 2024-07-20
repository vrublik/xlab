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
    def __init__(self, data: dict, user: User, model: str = 'gpt-4o', max_tokens: int = 50,
                 api_key=settings.OPENAI_API_KEY):
        self.model = model
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=api_key)
        self.data = data
        self.user = user

    def create_message(self, save=True) -> Message:
        chat_gpt_message = self.set_chat_gpt_messages(self.data)
        response = self.get_response_chat_gpt(chat_gpt_message)
        try:
            message = Message(
                user=self.user,
                request=self.data['message'],
                assistant_content=self.data.get('assistant_content'),
                response=response.choices[0].message.content
            )
        except ValueError as e:
            print(e)
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
            {"role": "user", "content": user_message}
        ]

        if assistant_content:
            messages.append({"role": "assistant", "content": assistant_content})

        return messages

    def get_response_chat_gpt(self, messages: List[dict]) -> ChatCompletion:
        try:
            response = self.client.chat.completions.create(messages=messages, model=self.model,
                                                           max_tokens=self.max_tokens)
        except APIStatusError as e:
            raise GenericAPIException(default_detail=json.loads(e.response.text), status_code=e.status_code)

        return response
