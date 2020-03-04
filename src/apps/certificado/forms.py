from django import forms

class DpiForm(forms.Form):
     dpi = forms.CharField(
        label='INGRESA TÚ DPI:',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))