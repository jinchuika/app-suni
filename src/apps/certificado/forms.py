from django import forms

class DpiForm(forms.Form):
     dpi = forms.CharField(
        label='Ingrese su Dpi    ',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))