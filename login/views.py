# views.py
from django.http import JsonResponse
from django.shortcuts import render
from .reconocimiento_facial import ReconocimientoFacial
from .reconocimiento_facial import Gestos

def login_view(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data', '')

        reconocimiento = ReconocimientoFacial()  
        reconocimiento.iniciar_reconocimiento()

        # Agregar la instanciación de la clase Gestos
        if reconocimiento.ventana_gestos:
            gestos = Gestos(reconocimiento.ventana_gestos)  
            gestos.iniciar_gestos()



    return render(request, 'login.html')

