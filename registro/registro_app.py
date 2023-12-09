import os
import base64
from django.conf import settings
from django.shortcuts import render
from PIL import Image
from io import BytesIO
from .models import Profile

def registrar_nuevo_vecino(request):
    if request.method == 'POST':
        name = request.POST.get('nombre')
        lastname = request.POST.get('apellido')
        image_data = request.FILES.get('image_data')

        if image_data:
            # Guardar la imagen en el modelo Profile
            persona = Profile(nombre=name, apellido=lastname)
            persona.save()

            media_path = os.path.join(settings.MEDIA_ROOT, 'profiles')
            if not os.path.exists(media_path):
                os.makedirs(media_path)

            image_name = f"{name}_{lastname}.jpg"
            image_path = os.path.join(media_path, image_name)

            # Guardar la imagen en disco después de decodificarla
            try:
                # Decodificar la imagen base64
                decoded_image = base64.b64decode(image_data.read())

                # Abrir la imagen utilizando PIL
                with Image.open(BytesIO(decoded_image)) as img:
                    # Guardar la imagen
                    img.save(image_path, format='JPEG')

                persona.imagen = f'profiles/{image_name}'
                persona.save()

                print(f"¡Registro exitoso! Imagen guardada en: {image_path}")
            except Exception as e:
                print(f"Error saving image: {e}")
        else:
            print("Error: 'image_data' is missing in the POST request")

    return render(request, 'registro.html')
