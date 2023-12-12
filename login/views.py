from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import FacialAuthenticationForm
from django.http import HttpResponse
import base64
import face_recognition
# Importa la biblioteca os para manejar rutas de archivos
import os

def facial_login(request):
    if request.method == 'POST':
        form = FacialAuthenticationForm(request.POST)
        image_data = request.POST.get('image_data')

        if form.is_valid() and image_data:
            # Decodificar la imagen base64
            img_data_decoded = base64.b64decode(image_data.split(',')[1])

            # Guardar la imagen en un archivo temporal
            image_path = "temp_image.jpg"
            with open(image_path, "wb") as img_file:
                img_file.write(img_data_decoded)

            try:
                # Cargar la imagen con face_recognition
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)

                if face_encodings:
                    # Comparar con las caras almacenadas en la carpeta de perfiles
                    profiles_folder = "profiles/"
                    profile_filenames = os.listdir(profiles_folder)

                    for profile_filename in profile_filenames:
                        # Cargar la imagen del perfil
                        profile_image = face_recognition.load_image_file(os.path.join(profiles_folder, profile_filename))
                        profile_encoding = face_recognition.face_encodings(profile_image)[0]

                        # Comparar las caras
                        match = face_recognition.compare_faces([profile_encoding], face_encodings[0], tolerance=0.5)

                        if match[0]:
                          
                            return HttpResponse("Autenticación exitosa.")
                           
                return HttpResponse("Error: No se encontró coincidencia con las caras almacenadas.")

            except Exception as e:
                return HttpResponse(f"Error: {str(e)}")

            finally:
                # Eliminar la imagen temporal
                os.remove(image_path)

    else:
        form = FacialAuthenticationForm()

    return render(request, 'facial_login.html', {'form': form})
