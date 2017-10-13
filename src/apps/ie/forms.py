from django import forms

from apps.ie.models import Laboratorio, Computadora, Serie


class LaboratorioCreateForm(forms.ModelForm):

    """Formulario para crear un :class:`Laboratorio`.
    """

    class Meta:
        model = Laboratorio
        fields = ('escuela',)


class LaboratorioUpdateForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = '__all__'
        exclude = ('escuela', 'organizacion')


class ComputadoraForm(forms.ModelForm):
    class Meta:
        model = Computadora
        fields = ('laboratorio',)
        widgets = {
        	'laboratorio': forms.HiddenInput()
        }


class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = '__all__'
        widgets = {
        	'computadora': forms.Select(attrs={'class': 'form-control'}),
        	'item': forms.Select(attrs={'class': 'select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(SerieForm, self).__init__(*args, **kwargs)
        self.fields['item'].label_from_instance = lambda obj: "%s" % '{} - {}'.format(obj.tipo, obj)
