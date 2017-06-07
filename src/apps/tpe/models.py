from decimal import Decimal
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User


class EquipamientoEstado(models.Model):
    estado = models.CharField(max_length=50)

    def __str__(self):
        return self.estado


class EquipamientoTipoRed(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo


class EquipamientoOs(models.Model):
    sistema_operativo = models.CharField(max_length=50)

    def __str__(self):
        return self.sistema_operativo

    class Meta:
        verbose_name = "Software para equipo"
        verbose_name_plural = "Software para equipo"


class Equipamiento(models.Model):
    id = models.IntegerField(primary_key=True)
    estado = models.ForeignKey(
        EquipamientoEstado,
        default=1,
        on_delete=models.PROTECT)
    escuela = models.ForeignKey('escuela.Escuela', related_name='equipamiento')
    fecha = models.DateField(default=timezone.now)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    renovacion = models.BooleanField(blank=True, default=False)
    servidor_khan = models.BooleanField(blank=True, default=False)
    servidor_os = models.ForeignKey(EquipamientoOs, null=True, blank=True, related_name='servidores', verbose_name='SO del servidor')
    cantidad_equipo = models.IntegerField(default=0)
    equipo_os = models.ForeignKey(EquipamientoOs, null=True, blank=True, verbose_name='SO de las PC')
    red = models.BooleanField(blank=True, default=False)
    tipo_red = models.ForeignKey(EquipamientoTipoRed, null=True, blank=True)
    fotos = models.BooleanField(default=False, blank=True)
    fotos_link = models.URLField(null=True, blank=True, verbose_name='Link a fotos')
    manual = models.BooleanField(default=False, blank=True)
    edulibre = models.BooleanField(default=False, blank=True)
    carta = models.BooleanField(default=False, blank=True)
    poblacion = models.ForeignKey('escuela.EscPoblacion', null=True, blank=True, verbose_name='Población')

    cooperante = models.ManyToManyField('mye.Cooperante', blank=True, related_name='equipamientos')
    proyecto = models.ManyToManyField('mye.Proyecto', blank=True, related_name='equipamientos')

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('escuela_equipamiento_detail', kwargs={'pk': self.escuela.id, 'id_equipamiento': self.id})


class EquipamientoSeguimiento(models.Model):
    equipamiento = models.ForeignKey(Equipamiento)
    usuario = models.ForeignKey(User)
    comentario = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)


class Garantia(models.Model):
    id = models.IntegerField(primary_key=True)
    equipamiento = models.ForeignKey(Equipamiento, related_name='garantias')
    fecha_vencimiento = models.DateField(null=True, blank=True)
    por_funsepa = models.BooleanField(blank=True)

    class Meta:
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"

    def get_absolute_url(self):
        return reverse_lazy('garantia_detail', kwargs={'pk': self.id})

    def __str__(self):
        return str(self.id)

    def get_vigente(self):
        if self.fecha_vencimiento:
            if timezone.now().date() > self.fecha_vencimiento:
                return False
            else:
                return True
        return False

    def get_costo_reparacion(self):
        return sum(t.get_costo_reparacion() for t in self.tickets.all())

    def get_costo_transporte(self):
        return sum(t.get_costo_transporte() for t in self.tickets.all())

    def get_costo(self):
        return sum(t.get_costo_total() for t in self.tickets.all())

    def get_ultimo_monitoreo(self):
        return self.equipamiento.monitoreos.all().order_by('fecha').last()


class TicketSoporte(models.Model):
    garantia = models.ForeignKey(Garantia, related_name='tickets')
    fecha_abierto = models.DateField(default=timezone.now)
    abierto_por = models.ForeignKey(User, related_name='tickets_abiertos')
    descripcion = models.TextField()
    cerrado = models.BooleanField(default=False, blank=True)
    fecha_cierre = models.DateField(null=True, blank=True)
    cerrado_por = models.ForeignKey(User, null=True, blank=True, related_name='tickets_cerrados')
    contacto_reporta = models.ForeignKey('escuela.EscContacto', related_name='tickets', null=True, blank=True)

    class Meta:
        verbose_name = "Ticket de soporte"
        verbose_name_plural = "Tickets de soporte"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('ticket_detail', kwargs={'pk': self.garantia.id, 'ticket_id': self.id})

    def get_costo_reparacion(self):
        return sum(r.get_costo() for r in self.reparaciones.all())

    def get_costo_transporte(self):
        return sum(t.costo for t in self.transportes.all())

    def get_costo_total(self):
        return self.get_costo_reparacion() + self.get_costo_transporte()


class TicketRegistroTipo(models.Model):
    tipo = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Soporte - Tipo de registro"
        verbose_name_plural = "Soporte - Tipos de registro"

    def __str__(self):
        return self.tipo


class TicketRegistro(models.Model):
    tipo = models.ForeignKey(TicketRegistroTipo)
    ticket = models.ForeignKey(TicketSoporte, related_name="registros")
    fecha = models.DateField(default=timezone.now)
    creado_por = models.ForeignKey(User)
    descripcion = models.TextField()
    foto = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Soporte - Registro de ticket"
        verbose_name_plural = "Soporte - Registro de tickets"

    def __str__(self):
        return '{} - {}'.format(self.ticket, self.id)

    def get_absolute_url(self):
        return reverse_lazy('ticket_detail', kwargs={'pk': self.ticket.garantia.id, 'ticket_id': self.ticket.id})


class TicketTransporteTipo(models.Model):
    tipo = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Tipo de transporte de garantías"
        verbose_name_plural = "Tipos de transporte de garantías"

    def __str__(self):
        return self.tipo


class TicketTransporte(models.Model):
    tipo = models.ForeignKey(TicketTransporteTipo)
    ticket = models.ForeignKey(TicketSoporte, related_name='transportes')
    costo = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('0.00'))
    fecha = models.DateField(default=timezone.now)
    usuario = models.ForeignKey(User, null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Transporte de garantías"
        verbose_name_plural = "Transportes de garantíass"

    def __str__(self):
        return 'G{} - {}'.format(self.ticket.garantia, self.tipo)

    def get_absolute_url(self):
        return reverse_lazy('ticket_detail', kwargs={'pk': self.ticket.garantia.id, 'ticket_id': self.ticket.id})


class DispositivoTipo(models.Model):
    tipo = models.CharField(max_length=75)

    class Meta:
        verbose_name = "Tipo de dispositivo"
        verbose_name_plural = "Tipos de dispositivo"

    def __str__(self):
        return self.tipo


class TicketReparacionTipo(models.Model):
    tipo = models.CharField(max_length=45)

    class Meta:
        verbose_name = "Tipo de reparación"
        verbose_name_plural = "Tipos de reparación"

    def __str__(self):
        return self.tipo


class TicketReparacionEstado(models.Model):
    estado = models.CharField(max_length=45)

    class Meta:
        verbose_name = "Estado de reparación"
        verbose_name_plural = "Estados de reparación"

    def __str__(self):
        return self.estado


class TicketReparacion(models.Model):
    ticket = models.ForeignKey(TicketSoporte, related_name='reparaciones')
    triage = models.PositiveIntegerField()
    tipo_dispositivo = models.ForeignKey(DispositivoTipo)
    tecnico_asignado = models.ForeignKey(User)
    estado = models.ForeignKey(TicketReparacionEstado)
    falla_reportada = models.TextField()
    falla_encontrada = models.TextField(null=True, blank=True)
    solucion_tipo = models.ForeignKey(TicketReparacionTipo, null=True, blank=True)
    solucion_detalle = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Reparación de garantía"
        verbose_name_plural = "Reparaciones de garantías"

    def __str__(self):
        return 'G{}-{}-{}'.format(self.ticket.garantia, self.tipo_dispositivo, self.triage)

    def get_absolute_url(self):
        return reverse_lazy('reparacion_update', kwargs={'pk': self.id})

    def get_costo(self):
        return sum(r.costo for r in self.repuestos.all() if r.autorizado)


class TicketReparacionRepuesto(models.Model):
    reparacion = models.ForeignKey(TicketReparacion, related_name="repuestos")
    tipo_dispositivo = models.ForeignKey(DispositivoTipo)
    costo = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('0.00'))
    justificacion = models.TextField(null=True, blank=True)
    fecha_solicitud = models.DateField(default=timezone.now)
    rechazado = models.BooleanField(default=False, blank=True)
    autorizado = models.BooleanField(default=False, blank=True)
    autorizado_por = models.ForeignKey(User, null=True, blank=True)
    fecha_autorizado = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Repuesto para reparación"
        verbose_name_plural = "Repuestos para reparación"

    def __str__(self):
        return '{} para {}'.format(self.tipo_dispositivo, self.reparacion)

    def get_absolute_url(self):
        return reverse_lazy('reparacion_update', kwargs={'pk': self.reparacion.id})


class Monitoreo(models.Model):
    equipamiento = models.ForeignKey(Equipamiento, related_name='monitoreos')
    creado_por = models.ForeignKey(User)
    fecha = models.DateField(default=timezone.now)
    comentario = models.TextField()

    class Meta:
        verbose_name = "Monitoreo"
        verbose_name_plural = "Registros de monitoreo"

    def __str__(self):
        return self.comentario[:15] + '...'
