from decimal import Decimal
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.escuela import models as escuela_m


class EquipamientoEstado(models.Model):
    estado = models.CharField(max_length=50)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    def __str__(self):
        return self.estado


class EquipamientoTipoRed(models.Model):
    tipo = models.CharField(max_length=50)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    def __str__(self):
        return self.tipo


class EquipamientoOs(models.Model):
    sistema_operativo = models.CharField(max_length=50)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    def __str__(self):
        return self.sistema_operativo

    class Meta:
        verbose_name = "Software para equipo"
        verbose_name_plural = "Software para equipo"


class Equipamiento(models.Model):
    id = models.IntegerField(primary_key=True)
    no_referencia = models.IntegerField(default=0, verbose_name='Numero de referencia de entrega')
    estado = models.ForeignKey(
        EquipamientoEstado,
        default=1,
        on_delete=models.PROTECT)
    escuela = models.ForeignKey(escuela_m.Escuela, related_name='equipamiento', on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    observacion = models.TextField(null=True, blank=True, verbose_name='Observaciones')
    renovacion = models.BooleanField(blank=True, default=False)
    servidor_khan = models.BooleanField(blank=True, default=False)
    servidor_os = models.ForeignKey(
        EquipamientoOs,
        null=True,
        blank=True,
        related_name='servidores',
        verbose_name='SO del servidor',
        on_delete=models.CASCADE)
    cantidad_equipo = models.IntegerField(default=0)
    equipo_os = models.ForeignKey(
        EquipamientoOs,
        null=True,
        blank=True,
        verbose_name='SO de las PC',
        on_delete=models.CASCADE)
    tablet_os = models.ForeignKey(
        EquipamientoOs,
        null=True,
        blank=True,
        related_name='os_tablet',
        verbose_name='SO de las tablet',
        on_delete=models.CASCADE)
    red = models.BooleanField(blank=True, default=False)
    tipo_red = models.ForeignKey(EquipamientoTipoRed, null=True, blank=True, on_delete=models.CASCADE)
    fotos = models.BooleanField(default=False, blank=True)
    fotos_link = models.URLField(null=True, blank=True, verbose_name='Link a fotos')
    manual = models.BooleanField(default=False, blank=True)
    edulibre = models.BooleanField(default=False, blank=True)
    carta = models.BooleanField(default=False, blank=True)
    poblacion = models.ForeignKey(
        escuela_m.EscPoblacion,
        null=True,
        blank=True,
        verbose_name='Población',
        on_delete=models.CASCADE)

    cooperante = models.ManyToManyField('mye.Cooperante', blank=True, related_name='equipamientos')
    proyecto = models.ManyToManyField('mye.Proyecto', blank=True, related_name='equipamientos')
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse_lazy(
            'escuela_equipamiento_detail',
            kwargs={'pk': self.escuela.id, 'id_equipamiento': self.id})

    @property
    def evaluacion(self):
        sumatoria = 0
        cantidad = 0
        for monitoreo in self.monitoreos.all():
            if monitoreo.porcentaje_evaluacion is not None:
                sumatoria += monitoreo.porcentaje_evaluacion
                cantidad += 1
        if cantidad > 0:
            return sumatoria / cantidad
        else:
            return None


class EquipamientoSeguimiento(models.Model):
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)


class Garantia(models.Model):
    id = models.IntegerField(primary_key=True)
    equipamiento = models.ForeignKey(Equipamiento, related_name='garantias', on_delete=models.CASCADE)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    por_funsepa = models.BooleanField(blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

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
    garantia = models.ForeignKey(Garantia, related_name='tickets', on_delete=models.CASCADE)
    fecha_abierto = models.DateField(default=timezone.now)
    abierto_por = models.ForeignKey(User, related_name='tickets_abiertos', on_delete=models.CASCADE)
    descripcion = models.TextField()
    cerrado = models.BooleanField(default=False, blank=True)
    fecha_cierre = models.DateField(null=True, blank=True)
    cerrado_por = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='tickets_cerrados',
        on_delete=models.CASCADE)
    contacto_reporta = models.ForeignKey(
        escuela_m.EscContacto,
        related_name='tickets',
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ticket de soporte"
        verbose_name_plural = "Tickets de soporte"

    def __str__(self):
        return str(self.id)

    def cubierto(self):
        """Indica si un ticket fue abierto antes de que la :class:`Garantia` finalice

        Returns:
            bool: Cubierto o no por la garantía
        """
        return self.garantia.equipamiento.fecha <= self.fecha_abierto <= self.garantia.fecha_vencimiento

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
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = "Soporte - Tipo de registro"
        verbose_name_plural = "Soporte - Tipos de registro"

    def __str__(self):
        return self.tipo


class TicketRegistro(models.Model):
    tipo = models.ForeignKey(TicketRegistroTipo, on_delete=models.CASCADE)
    ticket = models.ForeignKey(TicketSoporte, related_name="registros", on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    foto = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Soporte - Registro de ticket"
        verbose_name_plural = "Soporte - Registro de tickets"

    def __str__(self):
        return '{} - {}'.format(self.ticket, self.id)

    def get_absolute_url(self):
        return reverse_lazy(
            'ticket_detail',
            kwargs={'pk': self.ticket.garantia.id, 'ticket_id': self.ticket.id})


class TicketTransporteTipo(models.Model):
    tipo = models.CharField(max_length=30)
    creado_por = models.ForeignKey(User, blank=True, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Tipo de transporte de garantías"
        verbose_name_plural = "Tipos de transporte de garantías"

    def __str__(self):
        return self.tipo


class TicketTransporte(models.Model):
    tipo = models.ForeignKey(TicketTransporteTipo, on_delete=models.CASCADE)
    ticket = models.ForeignKey(TicketSoporte, related_name='transportes', on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('0.00'))
    fecha = models.DateField(default=timezone.now)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    comentario = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Transporte de garantías"
        verbose_name_plural = "Transportes de garantíass"

    def __str__(self):
        return 'G{} - {}'.format(self.ticket.garantia, self.tipo)

    def get_absolute_url(self):
        return reverse_lazy(
            'ticket_detail',
            kwargs={'pk': self.ticket.garantia.id, 'ticket_id': self.ticket.id})


class DispositivoTipo(models.Model):
    tipo = models.CharField(max_length=75)
    tpe_creada_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tpe_creada_por",default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Tipo de dispositivo"
        verbose_name_plural = "Tipos de dispositivo"

    def __str__(self):
        return self.tipo


class TicketReparacionTipo(models.Model):
    tipo = models.CharField(max_length=45)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = "Tipo de reparación"
        verbose_name_plural = "Tipos de reparación"

    def __str__(self):
        return self.tipo


class TicketReparacionEstado(models.Model):
    estado = models.CharField(max_length=45)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = "Estado de reparación"
        verbose_name_plural = "Estados de reparación"

    def __str__(self):
        return self.estado
    
class TipoSoporteTicket(models.Model):
    tipo = models.TextField(verbose_name='Tipo de soporte')
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)
    class Meta:
        verbose_name = "Tipo de soporte de ticket"
        verbose_name_plural = "Tipos de soporte de tickets"

    def __str__(self):
        return self.tipo

class TicketReparacion(models.Model):
    ticket = models.ForeignKey(TicketSoporte, related_name='reparaciones', on_delete=models.CASCADE)
    triage = models.PositiveIntegerField()
    tipo_dispositivo = models.ForeignKey(DispositivoTipo, on_delete=models.CASCADE)
    tecnico_asignado = models.ForeignKey(User, related_name='reparaciones_asignadas', on_delete=models.CASCADE)
    estado = models.ForeignKey(TicketReparacionEstado, on_delete=models.CASCADE)
    falla_reportada = models.TextField()
    falla_encontrada = models.TextField(null=True, blank=True)
    solucion_tipo = models.ForeignKey(TicketReparacionTipo, null=True, blank=True, on_delete=models.CASCADE)
    solucion_detalle = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)
    tipo_soporte = models.ForeignKey(TipoSoporteTicket,  on_delete=models.CASCADE, blank=True, null=True)

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
    reparacion = models.ForeignKey(TicketReparacion, related_name="repuestos", on_delete=models.CASCADE)
    tipo_dispositivo = models.ForeignKey(DispositivoTipo, on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('0.00'))
    justificacion = models.TextField(null=True, blank=True)
    fecha_solicitud = models.DateField(default=timezone.now)
    rechazado = models.BooleanField(default=False, blank=True)
    autorizado = models.BooleanField(default=False, blank=True)
    autorizado_por = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    fecha_autorizado = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Repuesto para reparación"
        verbose_name_plural = "Repuestos para reparación"

    def __str__(self):
        return '{} para {}'.format(self.tipo_dispositivo, self.reparacion)

    def get_absolute_url(self):
        return reverse_lazy('reparacion_update', kwargs={'pk': self.reparacion.id})


class Monitoreo(models.Model):
    equipamiento = models.ForeignKey(Equipamiento, related_name='monitoreos', on_delete=models.CASCADE)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    comentario = models.TextField()

    class Meta:
        verbose_name = "Monitoreo"
        verbose_name_plural = "Registros de monitoreo"

    def __str__(self):
        return self.comentario[:15] + '...'

    def get_absolute_url(self):
        return reverse_lazy('monitoreo_detail', kwargs={'pk': self.id})

    def crear_evaluaciones(self):
        preguntas = EvaluacionPregunta.objects.filter(activa=True)
        for pregunta in preguntas:
            punteo = (pregunta.maximo - pregunta.minimo) / 2
            self.evaluaciones.create(pregunta=pregunta, punteo=int(punteo),creado_por=self.creado_por)

    @property
    def porcentaje_evaluacion(self):
        cantidad = self.evaluaciones.count()
        if cantidad > 0:
            sumatoria = sum(evaluacion.porcentaje for evaluacion in self.evaluaciones.all())
            return sumatoria / cantidad
        else:
            return None


class EvaluacionPregunta(models.Model):
    pregunta = models.TextField()
    activa = models.BooleanField(default=True)
    minimo = models.PositiveIntegerField(default=1)
    maximo = models.PositiveIntegerField(default=5)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Pregunta de evaluación"
        verbose_name_plural = "Preguntas de evaluación"

    def __str__(self):
        return self.pregunta

    def clean(self):
        if self.minimo < 1:
            self.minimo += 1
            self.maximo += 1
        if self.minimo >= self.maximo:
            raise ValidationError({'maximo': 'El máximo debe ser mayor que el mínimo.'})


class EvaluacionMonitoreo(models.Model):
    monitoreo = models.ForeignKey(Monitoreo, related_name='evaluaciones', on_delete=models.CASCADE)
    pregunta = models.ForeignKey(EvaluacionPregunta, on_delete=models.CASCADE)
    punteo = models.PositiveSmallIntegerField()
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE,default=User.objects.get(username="Admin").pk)

    class Meta:
        verbose_name = "Evaluación de monitoreo"
        verbose_name_plural = "Evaluaciones de monitoreo"
        unique_together = ('monitoreo', 'pregunta')

    def __str__(self):
        return '{} - ({})'.format(self.pregunta, self.punteo)

    @property
    def porcentaje(self):
        return (self.punteo - 1) / (self.pregunta.maximo - self.pregunta.minimo) * 100

    def clean(self):
        if not self.pregunta.minimo <= self.punteo <= self.pregunta.maximo:
            raise ValidationError({'punteo': 'El punteo debe estar entre el rango de la pregunta.'})


class VisitaMonitoreo(models.Model):
    equipamiento = models.ForeignKey(Equipamiento, related_name='visitas_monitoreo', on_delete=models.CASCADE)
    fecha_visita = models.DateField(default=timezone.now, verbose_name='Fecha de Visita')
    hora_inicio = models.TimeField(default=timezone.now)
    hora_final = models.TimeField(default=timezone.now)
    comentario = models.TextField(null=True, blank=True)
    contacto = models.ForeignKey(
        escuela_m.EscContacto,
        related_name='visitas_contactos',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    fotos_link = models.URLField(null=True, blank=True, verbose_name='Link a fotografias')
    otras_personas = models.ManyToManyField(
        User, blank=True, related_name='visitas_varias',
        verbose_name='Otras personas que visitan'
    )
    encargado = models.ForeignKey(User, related_name="visitas_encargado", on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        TicketSoporte,
        null=True,
        blank=True,
        related_name='visitas_soporte',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Visita de monitoreo"
        verbose_name_plural = "Visitas de monitoreo"

    def get_absolute_url(self):
        return reverse_lazy('visita_monitoreo_detail', kwargs={'pk': self.id})

    def __str__(self):
        return str(self.id)
