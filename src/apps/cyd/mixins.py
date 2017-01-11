from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from apps.cyd.forms import CrHitoFormSet, CrAsistenciaFormSet


class BaseFormsetMixin(ContextMixin):
    formset_list = {}

    def get_context_data(self, **kwargs):
        context = super(BaseFormsetMixin, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        named_formsets = {}
        for prefix, formset_class in self.formset_list.items():
            named_formsets.update({prefix: formset_class(self.request.POST or None, prefix=prefix, instance=self.object)})
        return named_formsets

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        super(BaseFormsetMixin, self).form_valid(form)
        if len(named_formsets) < 1 and not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        else:
            self.object = form.save()
        for name, formset in named_formsets.items():
            print(len(formset))
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                # asistencias = formset.save(commit=False)
                # print(len(asistencias))
                for asistencia in formset:
                    asistencia = asistencia.save(commit=False)
                    asistencia.curso = self.object
                    print(asistencia)
                    asistencia.save()
        return redirect(self.get_success_url())


class CursoMixin(BaseFormsetMixin):
    formset_list = {
        'hito': CrHitoFormSet,
        'asistencia': CrAsistenciaFormSet}
