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

@api_view()
def get_user_id(request):
    player = Player.objects.get(id=2)
    return Response(player.avatar)


@api_view()
def get_users(reqest, username):
    players = Player.objects.filter(user__username__contains=username)[:5]
    return Response(PlayerSerializer(players, many=True).data)


@api_view()
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def check_profile(request, id):
    player = Player.objects.get(user=request.user)
    if player.id == id:
        return Response(status=200)
    return Response(status=500)

@api_view()
def get_player_data(request, id):
    player = Player.objects.get(id=id)
    return Response(PlayerSerializer(player).data)


@api_view()
def get_sessions(request, id):
    sessions1 = Session.objects.filter(player1=id)
    sessions2 = Session.objects.filter(player2=id)
    sessions3 = Session.objects.filter(player3=id)
    sessions4 = Session.objects.filter(player4=id)
    sessions = sessions1.union(sessions2, sessions3, sessions4).order_by('-date')
    serializer = SessionSerializer(sessions, many=True)
    return Response(serializer.data)

@api_view()
def get_id(request, username):
    user = User.objects.get(username=username)
    player = Player.objects.get(user=user)
    return Response(player.id)

@api_view(['POST'])
def send_session(request):
    serializer = SessionSerializer(data=request.data)
    if serializer.is_valid():
        session = Session(name=serializer.data['name'], result=serializer.data['result'], length=serializer.data['length'], player1=serializer.data['player1'], player2=serializer.data['player2'], player3=serializer.data['player3'], player4=serializer.data['player4'])
        session.save()
        return Response('ok')
    else:
        return Response('error')
