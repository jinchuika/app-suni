from django.views.generic.base import ContextMixin
from .forms import CrHitoFormSet, CrAsistenciaFormSet

class BaseFormsetMixin(ContextMixin):
	formset_list = {}
	def get_context_data(self, **kwargs):
		context = super(BaseFormsetMixin, self).get_context_data(**kwargs)
		context['named_formsets'] = self.get_named_formsets()
		return context

	def get_named_formsets(self):
		named_formsets = {}
		for prefix, formset_class in self.formset_list.items():
			named_formsets.update({prefix:  formset_class(self.request.POST or None, prefix=prefix, instance=self.object)})
		return named_formsets

	def form_valid(self, form):
		named_formsets = self.get_named_formsets()
		if not all((x.is_valid() for x in named_formsets.values())):
			return self.render_to_response(self.get_context_data(form=form))
		else:
			self.object = form.save()
		for name, formset in named_formsets.items():
			formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
			if formset_save_func is not None:
				formset_save_func(formset)
			else:
				formset.save()
		return redirect(self.success_url)

class CursoMixin(BaseFormsetMixin):
	formset_list = {
			'hito': CrHitoFormSet,
			'asistencia': CrAsistenciaFormSet,
		}
	def formset_hito_valid(self, formset):
		hitos = formset.save(commit=False)
		print(hitos)
		for obj in formset.deleted_objects:
			obj.delete()

		for hito in hitos:
			print(hito)
			hito.contacto = self.object
			hito.save()

	def formset_asistencia_valid(self, formset):
		asistencias = formset.save(commit=False)
		for obj in formset.deleted_objects:
			obj.delete()
		for asistencia in asistencias:
			asistencia.contacto = self.object
			asistencia.save()