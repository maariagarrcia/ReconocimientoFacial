import os
import base64
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

            # Crear una carpeta con el nombre de la persona si no existe
            folder_path = os.path.join('media', 'profiles', f"{name}_{lastname}")
            os.makedirs(folder_path, exist_ok=True)

            # Obtener la lista de archivos en la carpeta
            existing_files = os.listdir(folder_path)

            # Obtener el próximo número para la imagen
            next_number = len(existing_files) + 1

            # Guardar la imagen en la carpeta con el nombre numerado
            image_filename = f"{next_number}.jpg"
            image_path = os.path.join(folder_path, image_filename)

            # Guardar directamente el archivo en el sistema de archivos
            with open(image_path, 'wb') as f:
                f.write(img_data_decoded)

            # Crear el objeto Profile
            persona = Profile(nombre=name, apellido=lastname, imagen=os.path.join('profiles', f"{name}_{lastname}", image_filename))
            persona.save()

            print(f"¡Registro exitoso! Imagen guardada correctamente en {folder_path}")
        else:
            print("Error: 'image_data' is missing in the POST request")

    return HttpResponse("Registro completado")
