from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from .forms import SalidaEquipoFormSet

class SalidaContextMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(SalidaContextMixin, self).get_context_data(**kwargs)
		context['named_formsets'] = self.get_named_formsets()
		return context

	def get_named_formsets(self):
		return {
			'salida': SalidaEquipoFormSet(self.request.POST or None, prefix='salida', instance = self.object)
		}

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

	def formset_salida_valid(self, formset):
		salidas = formset.save(commit=False)
		print(salidas)
		for obj in formset.deleted_objects:
			obj.delete()

		for salida in salidas:
			print(salida)
			salida.salida = self.object
			salida.save()

	