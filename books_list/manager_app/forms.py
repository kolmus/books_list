from django import forms


class GoogleApiForm(forms.Form):
    title = forms.CharField(required=False, label="Tytuł")
    author = forms.CharField(required=False, label="Autor")

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        author = cleaned_data.get("author")
        if not title and not author:
            raise forms.ValidationError("Przynajmniej jedno pole musi być wypełnione")
        return cleaned_data
