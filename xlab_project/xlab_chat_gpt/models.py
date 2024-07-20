from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    request = models.TextField()
    assistant_content = models.TextField(blank=True, null=True)
    response = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Messages'
