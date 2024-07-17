import uuid
import qrcode
import json
import sys
from io import BytesIO
from django.db import models
from django.db.utils import OperationalError
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _

from easy_thumbnails import fields as et_fields

from apps.inventario import models  as inv_m
from apps.beqt import transacciones_beqt
from apps.crm import models as crm_m
from apps.tpe import models as tpe_m
from apps.escuela import models as escuela_m
from apps.mye import models as mye

# Create your models here.
class Entrada(models.Model):

    """Cualquier vía por la cual puede ingresar equipo al inventario.
    """

    tipo = models.ForeignKey(inv_m.EntradaTipo, on_delete=models.PROTECT, related_name='entradas_beqt')
    fecha = models.DateField()
    fecha_cierre = models.DateField(blank=True, null=True)
    en_creacion = models.BooleanField(default=True)
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entradas_creadas_beqt')
    recibida_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entradas_recibidas_beqt')
    proveedor = models.ForeignKey(crm_m.Donante, on_delete=models.PROTECT, related_name='entradas_beqt_proveedor')
    factura = models.PositiveIntegerField(default=0)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"

    def __str__(self):
        return str(self.id) 

    def get_absolute_url(self):
        if self.en_creacion:
            return reverse_lazy('entrada_beqt_update', kwargs={'pk': self.id})
        else:
            return reverse_lazy('entrada_beqt_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super(Entrada, self).save(*args, **kwargs)


class DispositivoTipoBeqt(models.Model):

    """Tipo de un :class:`Dispositivo`s
    En caso de que se marque `usa_triage` como `True`, el `slug` debe coincidir con
    los SLUG disponibles en los modelos que heredan :class:`Dispositivo`.
    """

    tipo = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    usa_triage = models.BooleanField(default=False)    
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Tipo de dispositivo"
        verbose_name_plural = "Tipos de dispositivo"
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.tipo

    def save(self, *args, **kwargs):
        """Valida que los los :class:`DispositivoTipo` que `usa_triage` tengan un `slug` valido.
        """
        if self.usa_triage:
            lista_slug = [m.SLUG_TIPO for m in DispositivoBeqt.__subclasses__()]
            if self.slug not in lista_slug:
                raise ValidationError(
                    ('El slug ingresado no coincide con los disponibles. Las opciones son: {}'.format(lista_slug)),
                    code='entrada_precio_total')
        super(DispositivoTipoBeqt, self).save(*args, **kwargs)


class EntradaDetalleBeqt(models.Model):

    """Detalle que indica la cantidad de cada tipo de equipo que ingresa en la :class:`Entrada`.
    Los campos de contabilidad indican el precio al ingresa el equipo cuando la entrada es una compra.
    El usuario ingresa el subtotal, el `precio_unitario` será calculado al dividir `precio_subtotal` / `total`.
    Los descuentos que se apliquen a la Entrada afectarán en el `precio_unitario`, por lo que ese dato
    se almacena en `precio_descontado`.

    El `precio_total` se calcula a partir de `precio_descontado` * `total`.
    """

    # Campos sobre inventario
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name='detalles_beqt')
    tipo_dispositivo = models.ForeignKey(DispositivoTipoBeqt, on_delete=models.PROTECT, related_name='detalles_entrada_beqt')
    total = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=50)
    dispositivos_creados = models.BooleanField(default=False, blank=True, verbose_name='Dispositivos creados') 
    qr_dispositivo = models.BooleanField(default=False, blank=True, verbose_name='Imprimir Qr Dispositivo')
    impreso = models.BooleanField(default=False, blank=True, verbose_name='Impreso')
    pendiente_autorizar = models.BooleanField(default=False, blank=True, verbose_name='pendiente')
    autorizado = models.BooleanField(default=False, blank=True, verbose_name='autorizado')
    # Creacion de fechas
    fecha_dispositivo = models.DateField(blank=True, null=True)    
    # Campos sobre contabilidad
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True) 
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # Registro
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT) 

    class Meta:
        verbose_name = "Detalle de entrada"
        verbose_name_plural = "Detalles de entrada"

    def __str__(self):
        return '{entrada} - {tipo}'.format(
            entrada=self.entrada,
            tipo=self.tipo_dispositivo)  

    def save(self, *args, **kwargs):
        """Se debe validar que el detalle de una entrada que involucre precio, por ejemplo, una compra,
        incluya el precio total.

        Los valores de los campos `precio_unitario` y `precio_descontado` pueden cambiar dependiendo de
        los descuentos que hayan sido aplicados a la entrada.
        El cálculo de todos los campos se realiza desde las funciones definidas en `signals.py`.
        """        
        if self.tipo_dispositivo.usa_triage is False:
            self.dispositivos_creados = True
            

        super(EntradaDetalleBeqt, self).save(*args, **kwargs)

    def crear_dispositivos(self, total=None):        
        if total is None:
            total = self.total
        # Busca el modelo del `tipo_dispositivo` del objeto actual
        modelo = DispositivoBeqt.obtener_modelo_hijo(self.tipo_dispositivo)
        creados = 0
        errores = 0
        for _ in range(0, total):
            try:
                transacciones_beqt.ingresar_dispositivo(
                    entrada=self.entrada,
                    modelo=modelo,
                    tipo=self.tipo_dispositivo,
                    entrada_detalle=self,
                    precio=self.precio_unitario
                    )
                creados = creados + 1
            except OperationalError:
                errores = errores + 1
        return {'creados': creados, 'errores': errores}   

    def get_absolute_url(self):
        return self.entrada.get_absolute_url()


class DispositivoBeqt(models.Model):

    """Cualquier elemento almacenado en la base de datos de inventario que puede ser entregado a una escuela.
    No debe existir una instancia de este modelo sin un objeto heredado del mismo.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    triage = models.SlugField(unique=True, blank=True, editable=False)
    tipo = models.ForeignKey(DispositivoTipoBeqt, on_delete=models.CASCADE)
    entrada = models.ForeignKey(Entrada, on_delete=models.PROTECT, related_name='dispositivos_beqt')
    entrada_detalle = models.ForeignKey(
        EntradaDetalleBeqt,
        on_delete=models.PROTECT,
        null=True,
        related_name='detalle_dispositivos')
    impreso = models.BooleanField(default=False, blank=True, verbose_name='Impreso')
    clase = models.ForeignKey(inv_m.DispositivoClase, on_delete=models.CASCADE, null=True, related_name='clase_dispositivos_beqt')
    estado = models.ForeignKey(
        inv_m.DispositivoEstado,
        on_delete=models.CASCADE,
        null=True,
        editable=True,
        default=inv_m.DispositivoEstado.PD
    )
    etapa = models.ForeignKey(
        inv_m.DispositivoEtapa,
        on_delete=models.PROTECT,
        null=True,
        editable=True,
        default=inv_m.DispositivoEtapa.AB
    )

    marca = models.ForeignKey(inv_m.DispositivoMarca, on_delete=models.CASCADE, null=True, blank=True)
    modelo = models.CharField(max_length=80, null=True, blank=True)
    serie = models.CharField(max_length=80, null=True, blank=True)
    codigo_rti = models.CharField(max_length=80, null=True, blank=True, verbose_name='codigo rti')
    codigo_qr = et_fields.ThumbnailerImageField(upload_to='qr_dispositivo_beqt', blank=True, null=True)
    tarima = models.ForeignKey(inv_m.Tarima, on_delete=models.PROTECT, blank=True, null=True, related_name='dispositivos_beqt')
    valido = models.BooleanField(default=True, blank=True, verbose_name='Válido')
    descripcion = models.TextField(null=True, blank=True)
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)    


    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"       
        indexes = [
            models.Index(fields=['triage']),
        ]

    def __str__(self):
        return str(self.triage)

    def save(self, *args, **kwargs):
        super(DispositivoBeqt, self).save(*args, **kwargs)
        if not self.codigo_qr:
            self.crear_qrcode()
            super(DispositivoBeqt, self).save(*args, **kwargs)

    def get_absolute_url(self):
        cast = self.cast()
        if cast:
            return cast.get_absolute_url()
        else:
            return ''

    def cast(self):
        """Se encarga de obtener el dispositivo del modelo que ha heredado este objeto.
        Por ejemplo, el CPU-1, M-3, etc.
        """
        for name in dir(self):
            try:
                attr = getattr(self, name)
                if isinstance(attr, self.__class__) and type(attr) != type(self):
                    return attr
            except:
                print("Error al cargar el modelo de {}".format(self.tipo))

    def crear_qrcode(self):
        """Genera le código QR para apuntar a la id del dispositivo
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=1,
        )
        data_qr = {
            'id': str(self.id),
            'triage': self.triage,
            'tipo': str(self.tipo)
        }
        qr.add_data(json.dumps(data_qr, ensure_ascii=False))
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer)
        filename = 'dispositivo-{}.png'.format(self.id)
        filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.getbuffer().nbytes, None)
        self.codigo_qr.save(filename, filebuffer)

    @classmethod
    def obtener_modelo_hijo(cls, tipo_dispositivo):
        """Obtiene el modelo hijo de `Dispositivo` a partir de un `DispositivoTipo`"""
        modelo = next(
            (
                f.related_model for f in cls._meta.get_fields()
                if f.one_to_one and f.related_model.SLUG_TIPO == tipo_dispositivo.slug
            ),
            None
        )
        if modelo is None:
            raise OperationalError('No es un dispositivo')
        return modelo

class DispositivoFalla(models.Model):
    dispositivo = models.ForeignKey(DispositivoBeqt, on_delete=models.CASCADE, related_name='fallas_beqt')
    descripcion_falla = models.TextField(verbose_name='Descripción de la falla')
    descripcion_solucion = models.TextField(null=True, blank=True, verbose_name='Descripción de la solución')
    fecha_inicio = models.DateTimeField(default=timezone.now, verbose_name='Fecha de inicio')
    fecha_fin = models.DateTimeField(blank=True, verbose_name='Fecha de fin', null=True)
    terminada = models.BooleanField(default=False, blank=True)
    reportada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='fallas_reportadas_beqt')
    reparada_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='fallas_reparadas_beqt',
        null=True,
        blank=True)

    class Meta:
        verbose_name = "DispositivoFalla"
        verbose_name_plural = "DispositivoFallas"

    def __str__(self):
        return 'F-{pk}'.format(pk=self.id)

    def get_absolute_url(self):
        return self.dispositivo.get_absolute_url()

class HDDBeqt(DispositivoBeqt):
    SLUG_TIPO = 'HDDB'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    puerto = models.ForeignKey(
        inv_m.DispositivoPuerto,
        on_delete=models.CASCADE,
        related_name='hdds_beqt',
        null=True,
        blank=True)
    capacidad = models.PositiveIntegerField(null=True, blank=True)
    medida = models.ForeignKey(inv_m.DispositivoMedida, null=True, blank=True)
    asignado = models.BooleanField(default=False, blank=True)


    class Meta:
        verbose_name = "HDD"
        verbose_name_plural = "HDDs"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_hdd_beqt'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('hdd_beqt_detail', kwargs={'triage': self.triage})

    @property
    def en_uso(self):
        """Indica si fue asignado a un :class:`Laptop`

        Returns:
            bool
        """
        return self.cpus.count() > 0 or self.laptops.count() > 0



class CargadorTabletBeqt(DispositivoBeqt):
    SLUG_TIPO = 'CTB'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    alimentacion = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Alimentacion')
    salida = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Salida voltaje')
   

    class Meta:
        verbose_name = "Cargador Tablet"
        verbose_name_plural = "Cargadores Tablets"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_cargador_tablet_beqt'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('cargador_tablet_beqt_detail', kwargs={'triage': self.triage})


class CaseTabletBeqt(DispositivoBeqt):
    SLUG_TIPO = 'ETB'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    compatibilidad = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Compatibilidad')
    color = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Color')
    estilo = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Estilo')
    material = models.CharField(max_length=80, null=True, blank=True, verbose_name='Material')
    dimensiones = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Dimensiones')
   

    class Meta:
        verbose_name = "Case Tablet"
        verbose_name_plural = "Cases Tablets"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_case_tablet_beqt'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('tablet_estuche_beqt_detail', kwargs={'triage': self.triage})

class ProtectorTabletBeqt(DispositivoBeqt):
    SLUG_TIPO = 'PTB'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    compatibilidad = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Compatibilidad')
    color = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Color')
    material = models.CharField(max_length=80, null=True, blank=True, verbose_name='Material')
    dimensiones = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Dimensiones')
   

    class Meta:
        verbose_name = "Protector Tablet"
        verbose_name_plural = "Protectores Tablets"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_protector_tablet_beqt'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('tablet_protector_beqt_detail', kwargs={'triage': self.triage})

class TabletBeqt(DispositivoBeqt):
    SLUG_TIPO = 'TB'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    version_sistema = models.ForeignKey(inv_m.VersionSistema, related_name='versiones_tablets_beqt', null=True, blank=True)
    so_id = models.ForeignKey(inv_m.Software, related_name='so_tablets_beqt', null=True, blank=True)
    almacenamiento = models.PositiveIntegerField(null=True, blank=True)
    medida_almacenamiento = models.ForeignKey(
        inv_m.DispositivoMedida,
        blank=True,
        null=True,
        related_name='almacenamiento_tablets_beqt')
    pulgadas = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    procesador = models.ForeignKey(inv_m.Procesador, blank=True, null=True)
    ram = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    medida_ram = models.ForeignKey(inv_m.DispositivoMedida, null=True, blank=True, related_name='ram_tables_beqt')
    almacenamiento_externo = models.BooleanField(default=False)
    cargador = models.ForeignKey(CargadorTabletBeqt, related_name='cargador_tablets_beqt', null=True, blank=True ,verbose_name='Cargador')
    estuche = models.ForeignKey(CaseTabletBeqt, related_name='case_tablets_beqt', null=True, blank=True, verbose_name='Case')


    class Meta:
        verbose_name = "Tablet"
        verbose_name_plural = "Tablets"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_tablet_beqt'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('tablet_beqt_detail', kwargs={'triage': self.triage})

class DispositivoRedBeqt(DispositivoBeqt):    
    SLUG_TIPO = 'DRB'
    indice = models.PositiveIntegerField(editable=False, unique=True)    
    cantidad_puertos = models.PositiveIntegerField(null=True, blank=True)
    puerto = models.ForeignKey(inv_m.DispositivoPuerto, null=True, blank=True)
    velocidad = models.PositiveIntegerField(null=True, blank=True)   


    class Meta:
        verbose_name = "Dispositivo de red"
        verbose_name_plural = "Dispositivos de red"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('red_beqt_detail', kwargs={'triage': self.triage})


class CargadorLaptopBeqt(DispositivoBeqt):
    SLUG_TIPO = 'CLB'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    voltaje = models.PositiveIntegerField(null=True, blank=True) 
 
    class Meta:
        verbose_name = "Cargador de laptop"
        verbose_name_plural = "Cargadores de laptops"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('cargador_laptop_beqt_detail', kwargs={'triage': self.triage})


class LaptopBeqt(DispositivoBeqt):
    SLUG_TIPO = 'LB'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    procesador = models.ForeignKey(inv_m.Procesador, on_delete=models.PROTECT, null=True, blank=True)
    version_sistema = models.ForeignKey(inv_m.VersionSistema, on_delete=models.PROTECT, null=True, blank=True)
    almacenamiento = models.PositiveIntegerField(null=True, blank=True)
    medida_almacenamiento = models.ForeignKey(
        inv_m.DispositivoMedida,
        blank=True,
        null=True,
        related_name='almacenamiento_laptop_beqt')
    disco_duro = models.ForeignKey(HDDBeqt, on_delete=models.PROTECT, null=True, blank=True, related_name='laptops_beqt')
    ram = models.PositiveIntegerField(null=True, blank=True)
    ram_medida = models.ForeignKey(inv_m.DispositivoMedida, null=True, blank=True)
    pulgadas = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    cargador = models.ForeignKey(CargadorLaptopBeqt, related_name='cargador_laptop_beqt', null=True, blank=True ,verbose_name='Cargador')
    servidor = models.BooleanField(default=False)
    


    class Meta:
        verbose_name = "Laptop"
        verbose_name_plural = "Laptops"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]
        db_table = 'dispositivo_laptop_beqt'

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('laptop_beqt_detail', kwargs={'triage': self.triage})


class AccessPointBeqt(DispositivoBeqt):
    SLUG_TIPO = 'APB'
    indice = models.PositiveIntegerField(editable=False, unique=True)
    cantidad_puertos = models.PositiveIntegerField(null=True, blank=True)
    puerto = models.ForeignKey(inv_m.DispositivoPuerto, null=True, blank=True)
    velocidad = models.PositiveIntegerField(null=True, blank=True)
    velocidad_medida = models.ForeignKey(inv_m.DispositivoMedida, null=True, blank=True)

    class Meta:
        verbose_name = "Access Point"
        verbose_name_plural = "Access Point"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('ap_beqt_detail', kwargs={'triage': self.triage})

#Nuevos dispositivos
class UpsBeqt(DispositivoBeqt):
    SLUG_TIPO = 'UPS'
    indice = models.PositiveIntegerField(editable=False, unique=True)   
    conexiones = models.PositiveIntegerField(null=True, blank=True)
    voltaje = models.CharField(max_length=80, null=True, blank=True,  verbose_name='Voltaje')

    class Meta:
        verbose_name = "Ups"
        verbose_name_plural = "Ups"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('ups_beqt_detail', kwargs={'triage': self.triage})

class RegletaBeqt(DispositivoBeqt):
    SLUG_TIPO = 'RB'
    indice = models.PositiveIntegerField(editable=False, unique=True)   
    conexiones = models.PositiveIntegerField(null=True, blank=True)
    voltaje =  models.CharField(max_length=80, null=True, blank=True,  verbose_name='Voltaje')
    regulador = models.BooleanField(default=False, blank=True, verbose_name='Con regulador')

    class Meta:
        verbose_name = "Regleta"
        verbose_name_plural = "Regletas"
        ordering = ['indice']
        indexes = [
            models.Index(fields=['indice']),
        ]

    def __str__(self):
        return self.triage

    def get_absolute_url(self):
        return reverse_lazy('regleta_beqt_detail', kwargs={'triage': self.triage})


class SalidaTipoBeqt(models.Model):
    nombre = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True,)
    necesita_revision = models.BooleanField(default=True, blank=True, verbose_name='Necesita revisión')
    especial = models.BooleanField(default=False, blank=True, verbose_name='especial')
    equipamiento = models.BooleanField(default=False, blank=True, verbose_name='equipamiento')
    renovacion = models.BooleanField(default=False, blank=True, verbose_name='equipamiento')
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Tipo de salida"
        verbose_name_plural = "Tipos de salida"

    def __str__(self):
        return self.nombre



class SalidaInventario(models.Model):
    tipo_salida = models.ForeignKey(SalidaTipoBeqt, on_delete=models.PROTECT)
    fecha = models.DateField(default=timezone.now)
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='salidas_beqt')
    en_creacion = models.BooleanField(default=True, verbose_name='En creación')
    entrega = models.BooleanField(default=True, verbose_name="Es entrega", blank=True)
    escuela = models.ForeignKey(
        escuela_m.Escuela,
        on_delete=models.PROTECT,
        related_name='entregas_beqt',
        null=True,
        blank=True)
    garantia = models.ForeignKey(
        tpe_m.TicketSoporte,
        on_delete=models.PROTECT,
        related_name='garantias_beqt',
        null=True,
        blank=True)
    observaciones = models.TextField(null=True, blank=True)
    necesita_revision = models.BooleanField(default=True, blank=True, verbose_name='Necesita revisión')
    beneficiario = models.ForeignKey(
        crm_m.Donante,
        on_delete=models.PROTECT,
        related_name='beneficiario_beqt',
        null=True,
        blank=True)
    estado = models.ForeignKey(inv_m.SalidaEstado, on_delete=models.PROTECT, related_name='estados_beqt',  null=True, blank=True)
    reasignado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reasignar_beqt', null=True, blank=True)
    no_salida = models.CharField(max_length=10, blank=True, editable=False, db_index=True)
    cooperante = models.ForeignKey(
        mye.Cooperante, on_delete=models.PROTECT,
        related_name='cooperante_beqt',
        null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    capacitada = models.BooleanField(default=False, verbose_name='Capacitada')
    meses_garantia = models.BooleanField(default=False, verbose_name='6 meses de Garantia')

    class Meta:
        verbose_name = "Salida"
        verbose_name_plural = "Salidas"

    def get_absolute_url(self):
        if self.en_creacion:
            return reverse_lazy('salidainventario_beqt_edit', kwargs={'pk': self.id})
        else:
            return reverse_lazy('salidainventario_beqt_detail', kwargs={'pk': self.id})

    def __str__(self):
        return str(self.no_salida)

    def crear_paquetes(self, cantidad, usuario, entrada, tipo_paquete=None):
        creados = 0
        indice_actual = self.paquetes_beqt.count()
        if self.tipo_salida.especial:
            if entrada.count() == 0:
                paquete = PaqueteBeqt(
                    salida=self,
                    indice=(1 + indice_actual),
                    creado_por=usuario,
                    cantidad=cantidad,
                    tipo_paquete=tipo_paquete,
                    aprobado=True
                )
                paquete.save()
            else:
                paquete = PaqueteBeqt(
                    salida=self,
                    indice=(1 + indice_actual),
                    creado_por=usuario,
                    cantidad=cantidad,
                    tipo_paquete=tipo_paquete,
                    aprobado=True
                    )
                paquete.save()
                for numero in entrada:
                    paquete.entrada.add(numero)
            creados += 1
            return creados
        else:
            if entrada.count() == 0:
                paquete = PaqueteBeqt(
                    salida=self,
                    indice=(1 + indice_actual),
                    creado_por=usuario,
                    cantidad=cantidad,
                    tipo_paquete=tipo_paquete,
                )
                paquete.save()
            else:
                paquete = PaqueteBeqt(
                    salida=self,
                    indice=(1 + indice_actual),
                    creado_por=usuario,
                    cantidad=cantidad,
                    tipo_paquete=tipo_paquete,
                    )
                paquete.save()
                for numero in entrada:
                    paquete.entrada.add(numero)
            creados += 1
            return creados


class SalidaComentarioBeqt(models.Model):
    salida = models.ForeignKey(SalidaInventario, on_delete=models.CASCADE, related_name='comentarios_beqt')
    comentario = models.TextField()
    fecha_revision = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = 'Comentario de revisión de salida control de calidad'
        verbose_name_plural = 'Comentarios de revisión de salida control de calidad'

    def __str__(self):
        return '{}'.format(self.comentario[15:])


class PaqueteTipoBeqt(models.Model):
    """Tipos de :class:`Paquete` a entregar. Puede incluir las partes básicas de una computadora, como CPU, Teclado,
    etc. o tipos más específicos como componentes de red
    """
    nombre = models.CharField(max_length=35, verbose_name='Nombre del tipo')
    tipo_dispositivo = models.ForeignKey(DispositivoTipoBeqt, verbose_name='Tipos de dispositivo', null=True, blank=True)
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Tipo de paquete"
        verbose_name_plural = "Tipos de paquete"

    def __str__(self):
        return self.nombre


class PaqueteBeqt(models.Model):
    """Un conjunto de :class:`Dispositivo` que se descargan del inventario.
    Por default, debería ser una computadora que contenga Mouse, Monitor, CPU, etc.
    Puede ser cualquier otro tipo de paquetes de dispositivos. Por ejemplo, un servidor
    puede tener además de los dipositivos básicos, un dispositivo de red."""
    salida = models.ForeignKey(SalidaInventario, on_delete=models.PROTECT, related_name="paquetes_beqt")
    fecha_creacion = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    indice = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField(default=0)
    tipo_paquete = models.ForeignKey(
        PaqueteTipoBeqt,
        on_delete=models.PROTECT,
        related_name='paquetes_beqt',
        null=True,
        blank=True)
    aprobado = models.BooleanField(default=False, blank=True)
    aprobado_kardex = models.BooleanField(default=False, blank=True)
    desactivado = models.BooleanField(default=False, blank=True)
    entrada = models.ManyToManyField(Entrada, related_name='tipo_entrada_beqt', blank=True, null=True)

    class Meta:
        verbose_name = "Paquete de salida"
        verbose_name_plural = "Paquetes de salida"
        unique_together = ('salida', 'indice')

    def __str__(self):
        return 'P{salida}-{indice}'.format(salida=self.salida, indice=self.indice)
        #return 'P{salida}'

    def aprobar(self, usuario):
        for paquete in self.asignacion.all():
            paquete.aprobado = True
            paquete.aprobado_por = usuario
            paquete.save()

    def get_absolute_url(self):
        return reverse_lazy('detalle_paquete_beqt', kwargs={'pk': self.id})

    def asignar_dispositivo(self, lista_dispositivos, usuario):
        """Asigna los dispositivo a los diferentes paquetes que se han creado
        """
        if not self.aprobado:
            for dispositivos in lista_dispositivos:
                if dispositivos.tipo == self.tipo_paquete.tipo_dispositivo:
                    asignar = DispositivoPaquete(
                        dispositivo=dispositivos,
                        paquete=self,
                        asignado_por=usuario
                    )
                    asignar.save()
                else:
                    raise OperationalError('El paquete ya fue aprobado')

class DispositivoPaquete(models.Model):
    """La asignación de un :class:`Dispositivo` a un :class:`Paquete`. Sirve para ser utilizado en control de calidad.
    Cada dispositivo de un paquete debe ser aprobado por control de calidad."""
    dispositivo = models.ForeignKey(DispositivoBeqt, on_delete=models.PROTECT, related_name='asignacion_beqt')
    paquete = models.ForeignKey(PaqueteBeqt, on_delete=models.PROTECT, related_name='asignacion_beqt')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    asignado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='paquetes_asignados_beqt')
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    aprobado = models.BooleanField(default=False)
    aprobado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='paquetes_aprobados_beqt')

    class Meta:
        verbose_name = "Asignación Dispositivo - Paquete"
        verbose_name_plural = "Asignaciones Dispositivo - Paquete"

    def __str__(self):
        return '{paquete} -> {dispositivo}'.format(
            paquete=self.paquete,
            dispositivo=self.dispositivo)


class RevisionSalidaBeqt(models.Model):
    salida = models.ForeignKey(SalidaInventario, on_delete=models.PROTECT, related_name='revisiones_beqt')
    revisado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_revision = models.DateTimeField(default=timezone.now, verbose_name='Fecha de revisión')
    anotaciones = models.TextField(null=True, blank=True, verbose_name='Anotaciones generales')
    aprobada = models.BooleanField(default=False, blank=True)
    tecnico = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='tecnicos_beqt'
        )

    class Meta:
        verbose_name = 'Revisión de salida en contabilidad'
        verbose_name_plural = 'Revisiones de salida en contabilidad'

    def __str__(self):
        return str(self.salida)

    def get_absolute_url(self):
        return reverse_lazy('revisionsalida_beqt_update', kwargs={'pk': self.id})


class RevisionComentarioBeqt(models.Model):
    revision = models.ForeignKey(RevisionSalidaBeqt, on_delete=models.CASCADE, related_name='comentarios_beqt')
    comentario = models.TextField()
    fecha_revision = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = 'Comentario de revisión'
        verbose_name_plural = 'Comentarios de revisión'

    def __str__(self):
        return '{}'.format(self.comentario[15:])



class SolicitudMovimientoBeqt(models.Model):
    """Solicitud de un técnico de área para cambiar cierta cantidad de dispositivos de la etapa. Por ejemplo:
    Un técnico solicitua cambiar 5 monitores de 'Almacenaje en bodega' a 'Tránsito'"""

    etapa_inicial = models.ForeignKey(inv_m.DispositivoEtapa, on_delete=models.PROTECT, related_name='solicitudes_inicial_beqt')
    etapa_final = models.ForeignKey(inv_m.DispositivoEtapa, on_delete=models.PROTECT, related_name='solicitudes_final_beqt')
    fecha_creacion = models.DateField(default=timezone.now)
    creada_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='solicitudes_movimiento_beqt')
    recibida_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recibida_por_beqt', null=True)
    autorizada_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='autorizaciones_movimiento_beqt',
        null=True)
    tipo_dispositivo = models.ForeignKey(DispositivoTipoBeqt, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    terminada = models.BooleanField(default=False)
    recibida = models.BooleanField(default=False)
    devolucion = models.BooleanField(default=False)
    rechazar = models.BooleanField(default=False)
    desecho = models.BooleanField(default=False)   
    observaciones = models.TextField(null=True, blank=True)
    no_salida = models.ForeignKey(SalidaInventario, on_delete=models.PROTECT, related_name='salida_inventario_beqt', null=True)
    

    class Meta:
        verbose_name = 'Solicitud de movimiento'
        verbose_name_plural = 'Solicitudes de movimiento'

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('solicitudmovimiento_beqt_detail', kwargs={'pk': self.id})

    def cambiar_etapa(self, lista_dispositivos, usuario):
        """Cambia el campo `etapa` de la lista de dispositivos recibida.
        En caso de que la solicitud ya haya sido terminada, no se puede volver a realizar esta operación.
        En el ciclo for se realiza la validación para no hacer cambios en dispositivos que no sean del tipo de
        que se está solicitando.
        """
        if not self.terminada:
            for dispositivo in lista_dispositivos:
                if dispositivo.tipo == self.tipo_dispositivo:
                    cambio = CambioEtapaBeqt(
                        solicitud=self,
                        dispositivo=dispositivo,
                        etapa_inicial=self.etapa_inicial,
                        etapa_final=self.etapa_final,
                        creado_por=usuario
                    )
                    cambio.save()
            validar = CambioEtapaBeqt.objects.filter(solicitud=self.id).count()
            if(validar == self.cantidad):
                print("Ya es la cantidad final")
                self.terminada = True
            else:
                print("Aun faltan dispositivos")

                # self.save()
        else:
            raise OperationalError('La solicitud ya fue terminada')


class CambioEtapaBeqt(models.Model):
    """Registra un movimiento de cambio de etapa en un :class:`Dispositivo`"""
    solicitud = models.ForeignKey(SolicitudMovimientoBeqt, on_delete=models.PROTECT, related_name='cambios_beqt')
    dispositivo = models.ForeignKey(DispositivoBeqt, on_delete=models.PROTECT, related_name='cambios_etapa_beqt')
    etapa_inicial = models.ForeignKey(inv_m.DispositivoEtapa, models.PROTECT, related_name='cambios_inicio_beqt')
    etapa_final = models.ForeignKey(inv_m.DispositivoEtapa, models.PROTECT, related_name='cambios_final_beqt')
    fechahora = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = 'Cambio de etapa'
        verbose_name_plural = 'Cambios de etapa'

    def __str__(self):
        return '{dispositivo} -> {final}'.format(
            dispositivo=self.dispositivo,
            final=self.etapa_final)

    def save(self, *args, **kwargs):
        if self.etapa_inicial != self.etapa_final:
            super(CambioEtapaBeqt, self).save(*args, **kwargs)
            self.dispositivo.etapa = self.etapa_final
            self.dispositivo.creada_por = self.creado_por
            self.dispositivo.tarima = None
            if self.solicitud.desecho:
                estado_desecho = inv_m.DispositivoEstado.objects.get(pk=inv_m.DispositivoEstado.DS)
                self.dispositivo.estado = estado_desecho
                self.dispositivo.creada_por =  self.creado_por
            self.dispositivo.save()


class AsignacionTecnico(models.Model):
    """Registra qué dispositivos puede manipular un técnico"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='tipos_dispositivos_beqt')
    tipos = models.ManyToManyField(DispositivoTipoBeqt, related_name='tipos_disponibles_beqt', blank=True)
    class Meta:
        verbose_name = 'Asignacion de técnico'
        verbose_name_plural = 'Asignaciones de técnicos'

    def __str__(self):
        return str(self.usuario)

    def get_absolute_url(self):
        return reverse_lazy('asignaciontecnico_beqt_update', kwargs={'pk': self.id})


class CambioEstadoBeqt(models.Model):
    dispositivo = models.ForeignKey(DispositivoBeqt, on_delete=models.CASCADE, related_name='cambios_estado_beqt')
    estado = models.ForeignKey(inv_m.DispositivoEstado, on_delete=models.PROTECT, related_name='cambios_beqt')
    fecha_hora = models.DateTimeField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = 'Cambio de estado'
        verbose_name_plural = 'Cambios de estado'

    def __str__(self):
        return '{} -> {}'.format(self.dispositivo, self.estado)

    def save(self, **kwargs):
        super(CambioEstadoBeqt, self).save(**kwargs)
        self.dispositivo.estado = self.estado
        self.dispositivo.save()

#Inventario interno de BEQT
