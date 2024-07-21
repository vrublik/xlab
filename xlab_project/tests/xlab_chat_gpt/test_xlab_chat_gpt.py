import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'testpassword'
    }


@pytest.fixture
def chat_message():
    return {
        'message': 'Is it chat GPT?'
    }


@pytest.fixture
def create_user(db, user_data):
    user = User.objects.create_user(username=user_data['username'], password=user_data['password'])
    return user


@pytest.fixture
def api_client():
    return APIClient()


def test_register(db, api_client, user_data):
    assert User.objects.filter(username=user_data['username']).exists() is False
    response = api_client.post(reverse('xlab_chat_gpt:register'), user_data, format='json')

    assert response.status_code == 201
    assert User.objects.filter(username=user_data['username']).exists() is True


def test_login(api_client, create_user, user_data):
    response = api_client.post(reverse('xlab_chat_gpt:login'), user_data, format='json')

    assert response.status_code == 200
    assert 'token' in response.data


def test_chat_no_token(api_client, chat_message):
    response = api_client.post(reverse('xlab_chat_gpt:chat'), chat_message, format='json', expect_errors=True)

    assert response.status_code == 401
    assert response.data['detail'] == 'Anonymous user, please login.'


def test_chat_with_token(api_client, create_user, user_data, chat_message):
    response_login = api_client.post(reverse('xlab_chat_gpt:login'), user_data, format='json')
    token = response_login.data['token']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    response = api_client.post(reverse('xlab_chat_gpt:chat'), chat_message, format='json', expect_errors=True)

    assert response.status_code == 200
    assert 'message_id' in response.data
    assert 'request' in response.data
    assert 'assistant_content' in response.data
    assert 'response' in response.data
    assert 'created_date' in response.data
    assert 'user' in response.data
