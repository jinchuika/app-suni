from django.contrib import admin
from django.apps import apps
from django.conf.urls import url
from django.http import HttpResponseRedirect
from .models import Dispositivo, Tarima, Sector

for model in apps.get_app_config('inventario').models.values():
	if model.__name__ not in ("Dispositivo","Tarima","Sector"):
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
				if not dispositivo.codigo_qr:
					print(dispositivo)
					dispositivo.crear_qrcode()
					dispositivo.save()
		else:
			print("No hay")
		return HttpResponseRedirect("../")

@admin.register(Tarima)
class TarimaAdmin(admin.ModelAdmin):
	change_list_template = "inventario/admin/tarima_changelist.html"

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [
			url(
		        r'^tarima/qr/$',
		        self.admin_site.admin_view(self.set_qr),
		        name='qr_tarima'
		    ),
		]
		return my_urls + urls

	def set_qr(self, request):
		tarimas = self.model.objects.all()
		print(tarimas)
		if len(tarimas) > 0:
			for tarima in tarimas:
				if not tarima.codigo_qr:
					print(tarima)
					tarima.crear_qrcode()
					tarima.save()
		else:
			print("No hay")
		return HttpResponseRedirect("../")

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
	change_list_template = "inventario/admin/sector_changelist.html"

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [
			url(
		        r'^sector/qr/$',
		        self.admin_site.admin_view(self.set_qr),
		        name='qr_sector'
		    ),
		]
		return my_urls + urls

	def set_qr(self, request):
		sectores = self.model.objects.all()
		print(sectores)
		if len(sectores) > 0:
			for sector in sectores:
				if not sector.codigo_qr:
					print(sector)
					sector.crear_qrcode()
					sector.save()
		else:
			print("No hay")
		return HttpResponseRedirect("../")

