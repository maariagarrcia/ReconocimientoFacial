from django.shortcuts import render
from app.forms import FaceRecognitionForm
from app.machinelearning import pipeline_model
from app.models import FaceRecognition
from django.conf import settings
import sklearn
import os


# Create your views here.

def index(request):
    form = FaceRecognitionForm()

    if request.method == "POST":
        form = FaceRecognitionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            save = form.save(commit=True) # commit=True: se guarda en la base de datos

            # extraer el id de la imagen guardada en la base de datos
            primary_key = save.pk
            imgobj = FaceRecognition.objects.get(pk=primary_key) # obtener el objeto de la imagen
            fileroot = str(imgobj.image) # obtener la ruta de la imagen
            filepath = os.path.join(settings.MEDIA_ROOT, fileroot)# obtener la ruta completa de la imagen
            results = pipeline_model(filepath) # ejecutar el modelo de machine learning
            print(results)

            return render(request, "index.html", {'form': form,"upload":True, "results":results})


    return render(request, "index.html", {'form': form,"upload":False})
