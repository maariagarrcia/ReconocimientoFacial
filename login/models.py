from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    imagen =  models.ImageField(upload_to='profiles/', blank=True, null=True)
