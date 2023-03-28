from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4


class Employees(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    contact = models.IntegerField()

    class Meta:
        ordering = ['id']


class CustomToken(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, to_field='username')
    token_key = models.CharField(max_length=100, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(minutes=2))
