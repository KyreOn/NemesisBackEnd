from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserForm


class RegView(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'Test.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
        else:
            return Response(form.errors)


class LoginView(APIView):
    form = UserForm()

    def get(self, request):
        return render(request, 'login.html', {'form': self.form})

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            return Response("logged")
        else:
            return Response(request.POST)


@login_required
def logout(request):
    logout(request)
