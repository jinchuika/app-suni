from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin, PermissionRequiredMixin
from .forms import FormEscuelaCrear, ContactoForm, ContactoTelefonoFormSet, ContactoMailFormSet
from .models import Escuela, EscContacto

class EscuelaCrear(LoginRequiredMixin, GroupRequiredMixin, CreateView):
	group_required = u"Administración"
	template_name = 'escuela/add.html'
	raise_exception = True
	redirect_unauthenticated_users = True
	form_class = FormEscuelaCrear

class EscuelaDetail(LoginRequiredMixin, DetailView):
	template_name = 'escuela/detail.html'
	model = Escuela

class EscuelaEditar(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = "escuela.change_escuela"
	model = Escuela
	template_name = 'escuela/add.html'
	form_class = FormEscuelaCrear
	raise_exception = True
	redirect_unauthenticated_users = True

class EscContactoCrear(LoginRequiredMixin, CreateView):
	template_name = 'escuela/contacto.html'
	model = EscContacto
	form_class = ContactoForm
	success_url = 'escuela_add'

	def get_context_data(self, **kwargs):
		context = super(EscContactoCrear, self).get_context_data(**kwargs)
		context['named_formsets'] = self.get_named_formsets()
		return context

	def get_named_formsets(self):
		return {
			'telefono': ContactoTelefonoFormSet(self.request.POST or None, prefix='telefono'),
			#'mail': ContactoMailFormSet(self.request.POST or None, prefix='mail'),
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

	def formset_telefono_valid(self, formset):
		telefonos = formset.save(commit=False)
		print(telefonos)
		for telefono in telefonos:
			print(telefono)
			telefono.contacto = self.object
			telefono.save()

	def formset_mail_valid(self, formset):
		mails = formset.save(commit=False)
		for mail in mails:
			mail.contacto = self.object
			mail.save()