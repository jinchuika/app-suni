from django import forms

from apps.dh.models import EventoDH


class EventoDHForm(forms.ModelForm):
    fecha = forms.DateField(
        initial='',
        widget=forms.TextInput(attrs={'class': 'datepicker', 'autocomplete': 'off'}))

    def __init__(self, *args, **kwargs):
        super(EventoDHForm, self).__init__(*args, **kwargs)
        self.fields['asistentes'].label_from_instance = lambda obj: "%s" % obj.get_full_name()

    class Meta:
        model = EventoDH
        fields = '__all__'
        exclude = ('creado_por', )
        widgets = {
            'titulo': forms.TextInput(),
            'hora_inicio': forms.TimeInput(attrs={'placeholder': '13:00'}),
            'hora_fin': forms.TimeInput(attrs={'placeholder': '15:00'}),
            'ubicacion': forms.TextInput(),
            'asistentes': forms.SelectMultiple(attrs={'class': 'select2'}),
            'cooperantes': forms.SelectMultiple(attrs={'class': 'select2'})
        }

    def clean(self):
        hora_inicio = self.cleaned_data.get("start_date")
        hora_fin = self.cleaned_data.get("end_date")
        if hora_inicio and hora_fin:
            if hora_fin < hora_inicio:
                msg = u"La hora a la que finaliza debe ser mayor a la de inicio."
                self._errors["hora_fin"] = self.error_class([msg])
