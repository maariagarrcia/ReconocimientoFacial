# camera/models.py
from django.db import models

class Profile(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
