from django.urls import path
from . import views


urlpatterns = [
    path('reg', views.RegView.as_view()),
    path('log', views.LoginView.as_view()),
    path('logout', views.user_logout),
    path('get_data', views.get_user_data)
]