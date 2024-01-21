from django.urls import path
from . import views


urlpatterns = [
    path('reg', views.RegView.as_view()),
    path('log', views.LoginView.as_view()),
    path('logout', views.user_logout),
    path('get_data/<str:username>', views.get_user_data),
    path('get_user', views.get_user),
    path('login', views.login, name='login'),
]