## Requirements
* Python 3.10

## Steps to run project locally
1. Download repository.
2. Create file `secret_settings.py` with the variable `OPENAI_API_KEY='your-openai-api-key'`
3. Create virtual env (Ubuntu):
   1. `sudo apt-get install python3.10-venv`
   2. `python3.10 -m venv myenv`
   3. `source myenv/bin/activate`
4. Use myenv to install requirements: `pip install -r requirements.txt`
5. Create db.sqlite3. Run command: `python manage.py migrate`
6. Run command: `python manage.py runserver`


## API Endpoints
## GET
## POST
* /api/register/
* /api/login/
* /api/chat/

### POST /api/register/

**Parameters**

|    Name    | Required |  Type  | Description |
|:----------:|:--------:|:------:|-------------|
| `username` | required | string | Username    |
| `password` | required | string | Password    |
| `email`    | optional | string | Email       |
**Response**
```
{
    "username": str,
    "email": str
}
```

### POST /api/login/

**Parameters**

|    Name    | Required |  Type  | Description |
|:----------:|:--------:|:------:|-------------|
| `username` | required | string | Username    |
| `password` | required | string | Password    |
**Response**
```
{
    "token": str
}
```

### POST /api/chat/

**Parameters**

|    Name     | Required |  Type  | Description                                                     |
|:-----------:|:--------:|:------:|-----------------------------------------------------------------|
|  `message`  | required | string | The text we send to chat gpt.                                   |
| `assistant` | optional | string | The way the chat gpt should respond. (Ex. "Answer like a dog.") |
**Response**
```
{
    "message_id": int,
    "request": str,
    "assistant_content": str,
    "response": str,
    "created_date": datetime,
    "user": int
}
```

## Websocket
`ws://127.0.0.1:8000/ws/?token=<user_token>`

**Parameters**

|    Name     | Required |  Type  | Description                                                     |
|:-----------:|:--------:|:------:|-----------------------------------------------------------------|
|  `message`  | required | string | The text we send to chat gpt.                                   |
| `assistant` | optional | string | The way the chat gpt should respond. (Ex. "Answer like a dog.") |
**Response**
```
{
    "message_id": int,
    "request": str,
    "assistant_content": str,
    "response": str,
    "created_date": datetime,
    "user": int
}
```

## Docker
#### Run commands:
1. `docker-compose build`
2. `docker-compose up`

You can check db in docker using following commands:
1. `docker-compose exec db sh`
2. `sqlite3 /root/xlab/data/db/db.sqlite3`
3. `select * from messages;`

## How to get API key:
https://platform.openai.com/api-keys

## Pytest
All tests in `xlab_project/tests/` directory 

> **Warning**  
> Enable VPN before running the tests

1. Run command: `pytest`
