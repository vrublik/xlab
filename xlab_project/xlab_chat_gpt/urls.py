from django.urls import path
from . import views

app_name = 'xlab_chat_gpt'

urlpatterns = [
    path('chat/', views.ChatAPIView.as_view(), name='chat'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
]
