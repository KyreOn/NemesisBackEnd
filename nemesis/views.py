from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth.models import User
from .models import Player, Session
from .serializers import UserSerializer, RegRequestSerializer, LoginRequestSerializer, TokenSerializer, PlayerSerializer, SessionSerializer
from rest_framework.authtoken.models import Token


class RegView(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'reg.html', {'form': form})

    def post(self, request):
        serializer = RegRequestSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']

            confirm = serializer.data['confirm']
            if password == confirm:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                player = Player(user=user)
                player.init()
                token = Token.objects.create(user=user)
                player.save()
                return Response(TokenSerializer(token).data)
            else:
                return Response('Пароли разные', status=500)
        else:
            return Response('Ошибка в данных', status=500)


class LoginView(APIView):
    form = UserForm()

    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        if serializer.is_valid():
            authenticated_user = authenticate(**serializer.validated_data)
            try:
                token = Token.objects.get(user=authenticated_user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=authenticated_user)
            return Response(TokenSerializer(token).data)
        else:
            return Response(serializer.errors, status=400)


def user_logout(request):
    logout(request)
    return redirect("/test")

@api_view(["GET"])
def get_user_data(request, username):
    user = User.objects.get(username=username)
    return Response(Player.objects.get(user=user).avatar)


@api_view()
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_user(request):
    player = Player.objects.get(user=request.user)
    return Response({'data': PlayerSerializer(player).data})

@api_view()
def get_player_data(request, username):
    user = User.objects.get(username=username)
    player = Player.objects.get(user=user)
    return Response(PlayerSerializer(player).data)

@api_view()
def get_sessions(request, username):
    sessions1 = Session.objects.filter(player1=username)
    sessions2 = Session.objects.filter(player2=username)
    sessions3 = Session.objects.filter(player3=username)
    sessions4 = Session.objects.filter(player4=username)
    sessions = sessions1.union(sessions2, sessions3, sessions4).order_by('-date')
    serializer = SessionSerializer(sessions, many=True)
    return Response(serializer.data)

@api_view()
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def check_profile(request, user_profile):
    user = request.user
    if (user.username == user_profile):
        return Response(status=200)
    return Response(status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_name(request):
    user = request.user
    user.username = request.data['username']
    user.save()
    return Response(user.username)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_avatar(request):
    player = Player.objects.get(user=request.user)
    player.avatarImage = request.data
    return Response(request.data)

