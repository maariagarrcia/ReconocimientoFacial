from django.urls import path
from .views import facial_login
# login/urls.py

urlpatterns = [
    path('facial-login/', facial_login, name='facial_login'),
]

