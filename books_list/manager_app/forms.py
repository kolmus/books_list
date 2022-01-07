from django import forms


class GoogleApiForm(forms.Form):
    title = forms.CharField(label="Tytuł")
    author = forms.CharField(label="Autor")
