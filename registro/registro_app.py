import base64
from django.core.files.base import ContentFile
from django.http import HttpResponse
from .models import Profile

def registrar_nuevo_vecino(request):
    if request.method == 'POST':
        name = request.POST.get('nombre')
        lastname = request.POST.get('apellido')
        image_data = request.POST.get('image_data')

        if image_data:
            # Decodificar la imagen base64
            img_data_decoded = base64.b64decode(image_data.split(',')[1])

            # Guardar la imagen en el modelo Profile
            persona = Profile(nombre=name, apellido=lastname)
            persona.save()

            # Asignar la imagen al campo 'imagen' del modelo
            persona.imagen.save(f"{name}_{lastname}.jpg", ContentFile(img_data_decoded), save=True)

            print("¡Registro exitoso! Imagen guardada correctamente.")
        else:
            print("Error: 'image_data' is missing in the POST request")

    return HttpResponse("Registro completado")
