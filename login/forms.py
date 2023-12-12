from django import forms

class FacialAuthenticationForm(forms.Form):
    image_data = forms.CharField(widget=forms.HiddenInput)
