from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from .services import MessageGPT
from .serializers import MessageSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=400)


class ChatAPIView(APIView):

    def post(self, request):
        message_gpt = MessageGPT(data=request.data, user=request.user)
        message = message_gpt.create_message()
        serializer = MessageSerializer(message)
        return Response(serializer.data)
