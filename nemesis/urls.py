from django.urls import path
from . import views


urlpatterns = [
    path('reg', views.RegView.as_view()),
    path('log', views.LoginView.as_view()),
    path('get_data/<str:username>', views.get_user_data),
    path('get_player/<int:id>', views.get_player_data),
    path('get_user', views.get_user),
    path('get_sessions/<int:id>', views.get_sessions),
    path('check_profile/<int:id>', views.check_profile),
    path('update_name', views.update_name),
    path('update_avatar', views.update_avatar),
    path('get_user_id', views.get_user_id),
    path('get_users/<str:username>', views.get_users )
]