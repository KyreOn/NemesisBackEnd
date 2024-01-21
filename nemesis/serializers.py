from rest_framework.serializers import Serializer, ModelSerializer, CharField
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Player, Session


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']


class LoginRequestSerializer(Serializer):
    model = User
    username = CharField(required=True)
    password = CharField(required=True)


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']


class PlayerSerializer(ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Player
        fields = '__all__'


class SessionSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'