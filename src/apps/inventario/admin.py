from django.contrib import admin
from django.apps import apps
from django.conf.urls import url
from django.http import HttpResponseRedirect
from .models import Dispositivo, Tarima, Sector, SalidaInventario, EntradaDetalle
from apps.tpe import models as tpe
from apps.conta import models as conta_m

for model in apps.get_app_config('inventario').models.values():
	if model.__name__ not in ("Dispositivo","Tarima","Sector","SalidaInventario"):
		admin.site.register(model)

@admin.register(SalidaInventario)
class SalidaInventarioAdmin(admin.ModelAdmin):
	change_list_template = "inventario/admin/salidainventario_changelist.html"

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [
			url(
		        r'^salida_inventario/escuelas/$',
		        self.admin_site.admin_view(self.set_escuelas),
		        name='salida_escuelas'
		    ),
		]
		return my_urls + urls

	def set_escuelas(self, request):
		salidas = self.model.objects.all().filter(entrega=1, escuela__isnull=True)
		print(salidas)
		if len(salidas) > 0:
			for salida in salidas:
				print(salida.id)
				entrega = tpe.Equipamiento.objects.filter(id=salida.id)
				print(entrega)
				if len(entrega) > 0:
					salida.escuela = entrega[0].escuela
					salida.save()
		else:
			print("No hay")
		return HttpResponseRedirect("../")

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
		    url(
		        r'^dispositivo/ingresar/$',
		        self.admin_site.admin_view(self.set_ingreso_conta),
		        name='ingresar_conta'
		    ),
		]
		return my_urls + urls

	def set_qr(self, request):
		dispositivos = self.model.objects.all().filter(valido=True)
		print(dispositivos)
		if len(dispositivos) > 0:
			for dispositivo in dispositivos:
				if not dispositivo.codigo_qr:
					dispositivo.crear_qrcode()
					dispositivo.save()
		else:
			print("No hay")
		return HttpResponseRedirect("../")

	def set_ingreso_conta(self, request):
		dispositivos = self.model.objects.all()
		if len(dispositivos) > 0:
			for dispositivo in dispositivos:
				periodo_fiscal = conta_m.PeriodoFiscal.objects.get(fecha_inicio__lte = dispositivo.entrada.fecha, fecha_fin__gte= dispositivo.entrada.fecha)
				entrada_detalle =  EntradaDetalle.objects.filter(entrada = dispositivo.entrada, tipo_dispositivo = dispositivo.tipo)
				precio=None

				if periodo_fiscal and len(entrada_detalle) > 0:
					if not entrada_detalle[0].precio_unitario or entrada_detalle[0].precio_unitario == 0.0:
						precio_estandar = conta_m.PrecioEstandar.objects.get(
							tipo_dispositivo=dispositivo.tipo,
							periodo=periodo_fiscal,
							inventario=conta_m.PrecioEstandar.DISPOSITIVO)
						precio = precio_estandar.precio
					else:
						precio = entrada_detalle[0].precio_unitario

					#generar registros contables.
					nuevo_precio = conta_m.PrecioDispositivo(
						dispositivo=dispositivo,
						periodo=periodo_fiscal,
						precio=precio)
					nuevo_precio.save()

					movimiento = conta_m.MovimientoDispositivo(
						fecha=dispositivo.entrada.fecha,
						dispositivo=dispositivo,
						periodo_fiscal=periodo_fiscal,
						tipo_movimiento=conta_m.MovimientoDispositivo.ALTA,
						referencia='Entrada {}'.format(dispositivo.entrada),
						precio=precio)
					movimiento.save()

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
		if len(tarimas) > 0:
			for tarima in tarimas:
				if not tarima.codigo_qr:
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
		if len(sectores) > 0:
			for sector in sectores:
				if not sector.codigo_qr:
					sector.crear_qrcode()
					sector.save()
		else:
			print("No hay")
		return HttpResponseRedirect("../")

