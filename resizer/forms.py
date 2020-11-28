from django import forms

class SizeForm(forms.Form):
    height = forms.IntegerField(required=False)
    width = forms.IntegerField(required=False)