from app.models import FaceRecognition
from django import forms

class FaceRecognitionForm(forms.ModelForm):
    class Meta:
        model = FaceRecognition
        fields = ['image']
        