from django import forms

class FileFieldForm(forms.Form):
    file_field1 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    file_field2 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
