from django import forms
from apps.inventario import models as inv_m


class TecladoForm(forms.ModelForm):
    class Meta:
        model = inv_m.Teclado
        fields = '__all__'
        exclude = ['indice', 'entrada', 'tipo']
        widgets = {
            'codigo_qr': forms.URLInput(attrs={'class': 'form-control'})
                   }


class DispositivoFallaForm(forms.ModelForm):
    class Meta:
        model = inv_m.DispositivoFalla
        fields = ('dispositivo', 'descripcion_falla',)
        widgets = {
            'dispositivo': forms.HiddenInput(),
            'descripcion_falla': forms.Textarea(attrs={'class': 'form-control'})
        }


class AsignacionTecnicoForm(forms.ModelForm):
    """Formulario para manipulación de :class:`AsignacionTecnico`"""
    tipos = forms.ModelMultipleChoiceField(
        queryset=inv_m.DispositivoTipo.objects.filter(usa_triage=True),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = inv_m.AsignacionTecnico
        fields = '__all__'
        widgets = {
            'usuario': forms.Select(attrs={'class': 'select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(AsignacionTecnicoForm, self).__init__(*args, **kwargs)
        self.fields['usuario'].label_from_instance = lambda usuario: usuario.get_full_name()
