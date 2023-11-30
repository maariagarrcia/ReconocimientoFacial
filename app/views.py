from django.shortcuts import render
from app.forms import FaceRecognitionForm
from app.machinelearning import pipeline_model
from app.models import FaceRecognition
from django.conf import settings


# Create your views here.

def index(request):
    form = FaceRecognitionForm()

    if request.method == "POST":
        form = FaceRecognitionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            save = form.save(commit=True)

            primary_key = save.pk
            imgobj = FaceRecognition.objects.get(pk=primary_key)
            fileroot = str(imgobj.image)
            filepath = settings.MEDIA_ROOT + fileroot
            results = pipeline_model(filepath)
            print(results)

    return render(request, "index.html", {'form': form})
