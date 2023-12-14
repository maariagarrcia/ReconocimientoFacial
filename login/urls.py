from django.urls import path
from .views import facial_login, video_feed,login,grupo,index,reconocimiento_view
# login/urls.py

urlpatterns = [
    path('facial-login/', facial_login, name='facial_login'),
    path('video-feed/', video_feed, name='video_feed'),
    path('l/', login, name='login'),
    path('g/', grupo, name='grupo'),
    path('i/', index, name='index'),
    path('r/', reconocimiento_view, name='reconocimiento_view'),


]

