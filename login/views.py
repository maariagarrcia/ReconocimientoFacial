# views.py
from django.http import JsonResponse
from django.shortcuts import render

def login_view(request):
    if request.method == 'POST':
        image_data = request.POST.get('image_data', '')
        
        # Procesa la imagen como desees, por ejemplo, puedes guardarla en el servidor
        # y realizar el reconocimiento facial aquí

        # Simplemente para demostración, aquí se retorna un JSON indicando si se detectó un rostro o no
        face_detected = True  # Cambia esto según tu lógica de reconocimiento facial
        
        return JsonResponse({'face_detected': face_detected})

    return render(request, 'login.html')
