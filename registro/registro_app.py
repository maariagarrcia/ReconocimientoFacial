import os
from django.conf import settings
from django.shortcuts import render
from .models import Profile

def registrar_nuevo_vecino(request):
    if request.method == 'POST':
        name = request.POST.get('nombre')
        lastname = request.POST.get('apellido')
        image_data = request.POST.get('image_data')

        if image_data:
            # Guardar la imagen en el modelo Profile
            persona = Profile(nombre=name, apellido=lastname)
            persona.save()

            media_path = os.path.join(settings.MEDIA_ROOT, 'profiles')
            if not os.path.exists(media_path):
                os.makedirs(media_path)

            image_name = f"{name}_{lastname}.jpg"
            image_path = os.path.join(media_path, image_name)

            # Guardar la imagen en disco sin decodificar
            try:
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_data)
            except Exception as e:
                print(f"Error saving image: {e}")

            persona.imagen = f'profiles/{image_name}'
            persona.save()

            print(f"¡Registro exitoso! Imagen guardada en: {image_path}")
        else:
            print("Error: 'image_data' is missing in the POST request")

    return render(request, 'registro.html')
