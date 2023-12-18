from django.urls import path
from .views import facial_login,grupo,index,reconocimiento_view
# login/urls.py

urlpatterns = [
    path('i/', index, name='index'),


]

