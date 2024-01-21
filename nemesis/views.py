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
from .models import Player
from .serializers import UserSerializer, LoginRequestSerializer, TokenSerializer
from rest_framework.authtoken.models import Token


class RegView(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'reg.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            player = Player(user=user)
            player.init()
            player.save()
            return Response("reg")
        else:
            return Response("reg errors")


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
def get_user(request):
    if request.user.is_authenticated:
        return Response({'data': UserSerializer(request.user).data})
