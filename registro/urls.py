# camera/urls.py
from django.urls import path
from .views import index, registro

urlpatterns = [
    path('', index, name='index'),
    path('registro/', registro, name='registro'),
]


