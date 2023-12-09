# camera/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile
from .registro_app import registrar_nuevo_vecino

def index(request):
    return render(request, 'base.html')

def registro(request):
    if request.method == 'POST':
        # Llama a registrar_nuevo_vecino con el objeto request
        registrar_nuevo_vecino(request)
        return HttpResponse("¡Registro exitoso!")

    return render(request, 'registro.html')
