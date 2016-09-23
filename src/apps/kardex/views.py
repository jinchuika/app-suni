from django.shortcuts import render, redirect
from apps.kardex.models import *
from apps.kardex.forms import *
from django.views.generic.edit import CreateView
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy



def index(request):
	equipo = Equipo.objects.filter()
	if request.method=='POST':
		formequipo = FormularioEquipo(request.POST or None)
		if formequipo.is_valid():
			new_article = formequipo.save()
		return redirect('kardex_equipo')
	else:
		formequipo = FormularioEquipo()

	context={
		"formequipo": formequipo,
		"equipo_load" : equipo,
	}
	return render(request, 'kardex/index.html', context)


#entrada del equipo
class EntradaCreate(LoginRequiredMixin, CreateView):
	model = Entrada
	form_class = FormularioEntrada
	template_name = "kardex/entrada.html"
	success_url = reverse_lazy('kardex_equipo')

	def form_valid(self, form):
		self.object = form.save(commit = False)
		if self.object.cantidad <= 0:
			return self.form_invalid(form)
		else:
			self.object.save()
			return super(EntradaCreate, self).form_valid(form)


#Salida del equipo
class SalidaCreate(LoginRequiredMixin, CreateView):
	model = Salida
	form_class = FormularioSalida
	template_name = "kardex/salida.html"
	success_url = reverse_lazy('kardex_equipo')

	def form_valid(self, form):
		self.object = form.save(commit = False)
		if self.object.cantidad >  self.object.equipo.existencia:
			return self.form_invalid(form)
		else:
			self.object.save()
			return super(SalidaCreate, self).form_valid(form)




class ProveedorCreate(LoginRequiredMixin, CreateView):
	model = Proveedor
	form_class = FormularioProveedor
	template_name = "kardex/proveedor.html"