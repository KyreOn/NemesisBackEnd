import datetime
import random

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TestObject(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    gameCount = models.IntegerField(default=0)
    last_online = models.DateTimeField(auto_now_add=True)
    in_game_time = models.IntegerField(default=0)
    avatar = models.CharField(max_length=100)

    def init(self):
        randomId = random.randint(0, 3)
        if randomId == 0:
            self.avatar = "https://drive.google.com/uc?export=view&id=1WLG2Iggd4w7sEiuWizE7W5TXj3rdr4WG"
        elif randomId == 1:
            self.avatar = "https://drive.google.com/uc?export=view&id=1mZxE8IJUMV3AlLYaLS0wqwTmU-UyN3nT"
        elif randomId == 2:
            self.avatar = "https://drive.google.com/uc?export=view&id=11nN4I0cd7Fv83M-ZcJf9U6h3ZMS5xsXK"
        else:
            self.avatar = "https://drive.google.com/uc?export=view&id=1NLPv8nQIAvOBF5dD6yrshtYcMMBotSlt"
        self.save()

class Session(models.Model):
    name = models.CharField(max_length=50, default='session_name')
    date = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
    player1 = models.IntegerField(default=1)
    player2 = models.IntegerField(default=1)
    player3 = models.IntegerField(default=1)
    player4 = models.IntegerField(default=1)
