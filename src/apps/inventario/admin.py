from django.contrib import admin
from django.apps import apps
from django.conf.urls import url
from django.http import HttpResponseRedirect
from .models import Dispositivo

for model in apps.get_app_config('inventario').models.values():
	if model.__name__ != "Dispositivo":
		admin.site.register(model)

@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
	change_list_template = "inventario/admin/dispositivo_changelist.html"

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [
			url(
		        r'^dispositivo/qr/$',
		        self.admin_site.admin_view(self.set_qr),
		        name='qr'
		    ),
		]
		return my_urls + urls

	def set_qr(self, request):
		dispositivos = self.model.objects.all().filter(valido=True)
		print(dispositivos)
		if len(dispositivos) > 0:
			for dispositivo in dispositivos:
				print(dispositivo)
			if not dispositivo.codigo_qr:
				dispositivo.crear_qrcode()
		else:
			print("No hay")
		return HttpResponseRedirect("../")


