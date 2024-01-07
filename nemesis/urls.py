from django.urls import path
from . import views


urlpatterns = [
    path('test', views.RegView.as_view()),
    path('log', views.LoginView.as_view())
]