import random

from django.db import models
from django.contrib.auth.models import User


class TestObject(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)


class Player(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    desc = models.IntegerField(default=0)

    def init(self):
        self.desc = random.randint(0, 10)
        self.save()