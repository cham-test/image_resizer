from django import forms

class SizeForm(forms.Form):
    height = forms.IntegerField(required=False)
    width = forms.IntegerField(required=False)

class UploadForm(forms.Form):
    url = forms.URLField(required=False)
    image = forms.ImageField(required=False)
