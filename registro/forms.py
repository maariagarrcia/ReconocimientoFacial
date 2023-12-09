# myapp/forms.py
from django import forms

class RegistrationForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    image_data = forms.ImageField()
