from django import forms

class FileFieldForm(forms.Form):
    file_field1 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    file_field2 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class ShowClusersForm(forms.Form):
    cluster_1 = forms.IntegerField(label='ID of first cluster from above')
    cluster_2 = forms.IntegerField(label='ID of second cluster from above')
