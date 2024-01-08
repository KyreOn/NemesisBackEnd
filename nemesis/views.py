from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth.models import User
from .models import Player

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
            return Response(form.errors)


class LoginView(APIView):
    form = UserForm()

    def get(self, request):
        return render(request, 'login.html', {'form': self.form})

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return Response("logged")
        else:
            return Response(request.POST)


def user_logout(request):
    logout(request)
    return redirect("/test")

@api_view(["POST"])
def get_user_data(request):
    user = User.objects.get(username=request.POST.get('username'))
    return Response(Player.objects.get(user=user).desc)