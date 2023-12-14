from django.urls import path
from .views import facial_login,grupo,index,reconocimiento_view
# login/urls.py

urlpatterns = [
    path('facial-login/', facial_login, name='facial_login'),
    path('g/', grupo, name='grupo'),
    path('i/', index, name='index'),
    path('r/', reconocimiento_view, name='reconocimiento_view'),


]

