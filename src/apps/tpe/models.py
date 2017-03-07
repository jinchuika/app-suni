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


class Equipamiento(models.Model):
    id = models.IntegerField(primary_key=True)
    estado = models.ForeignKey(
        EquipamientoEstado,
        default=1,
        on_delete=models.PROTECT)
    escuela = models.ForeignKey('escuela.Escuela', related_name='equipamiento')
    fecha = models.DateField(default=timezone.now)
    observacion = models.TextField(null=True, blank=True)
    renovacion = models.BooleanField(blank=True, default=False)
    servidor_khan = models.BooleanField(blank=True, default=False)
    cantidad_equipo = models.IntegerField(default=0)
    red = models.BooleanField(blank=True, default=False)
    tipo_red = models.ForeignKey(EquipamientoTipoRed, null=True, blank=True)
    fotos = models.BooleanField(default=False, blank=True)
    manual = models.BooleanField(default=False, blank=True)
    edulibre = models.BooleanField(default=False, blank=True)
    carta = models.BooleanField(default=False, blank=True)

    cooperante = models.ManyToManyField('mye.Cooperante', blank=True)
    proyecto = models.ManyToManyField('mye.Proyecto', blank=True)

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
    equipamiento = models.ForeignKey(Equipamiento, related_name='garantias')
    fecha_vencimiento = models.DateField()

    class Meta:
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"

    def get_absolute_url(self):
        return reverse_lazy('garantia_detail', kwargs={'pk': self.id})

    def __str__(self):
        return str(self.id)

    def get_vigente(self):
        if timezone.now().date() > self.fecha_vencimiento:
            return False
        else:
            return True


class TicketSoporte(models.Model):
    garantia = models.ForeignKey(Garantia, related_name='tickets')
    fecha_abierto = models.DateField(default=timezone.now)
    abierto_por = models.ForeignKey(User)
    fecha_cierre = models.DateField(null=True, blank=True)
    cerrado = models.BooleanField(default=False, blank=True)
    descripcion = models.TextField()

    class Meta:
        verbose_name = "Soporte - Ticket"
        verbose_name_plural = "Soporte - Tickets"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('ticket_detail', kwargs={'pk': self.garantia.id, 'ticket_id': self.id})

    def costos(self):
        envio = sum(registro.costo_envio for registro in self.registros.all())
        return envio


class TicketRegistroTipo(models.Model):
    tipo = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Soporte - Tipo de registro"
        verbose_name_plural = "Soporte - Tipos de registro"

    def __str__(self):
        return self.tipo


class TicketRegistro(models.Model):
    ticket = models.ForeignKey(TicketSoporte, related_name="registros")
    fecha = models.DateField(default=timezone.now)
    usuario = models.ForeignKey(User)
    tipo = models.ForeignKey(TicketRegistroTipo)
    descripcion = models.TextField()
    costo_reparacion = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('0.00'))
    costo_envio = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = "Soporte - Registro de ticket"
        verbose_name_plural = "Soporte - Registro de tickets"

    def __str__(self):
        return str(self.ticket) + " - " + str(self.id)

    def get_absolute_url(self):
        return reverse_lazy('ticket_detail', kwargs={'pk': self.ticket.garantia.id, 'ticket_id': self.ticket.id})


class Monitoreo(models.Model):
    equipamiento = models.ForeignKey(Equipamiento, related_name='monitoreos')
    creado_por = models.ForeignKey(User)
    fecha = models.DateField(default=timezone.now)
    comentario = models.TextField()

    class Meta:
        verbose_name = "Monitoreo"
        verbose_name_plural = "Registro de monitoreo"

    def __str__(self):
        return self.comentario[:15] + '...'
