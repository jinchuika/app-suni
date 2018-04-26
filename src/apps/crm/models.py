from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class DonanteTipo(models.Model):
    """Tipos de Donante que pueden existir Grande, mediano ,individual
    """
    tipo = models.CharField(max_length=20, verbose_name="Tipo de Donante")

    class Meta:
        verbose_name = "Tipo de Donante"
        verbose_name_plural = "Tipos de Donantes"

    def __str__(self):
        return self.tipo

    def get_absolute_url(self):
        return reverse_lazy('donante_edit', kwargs={'pk': self.donante.id})


class OfertaTipo(models.Model):
    """ Tipo de oferta que se va a utilizar
    """
    oferta_tipo = models.CharField(max_length=50, blank=True, verbose_name="Tipo de Oferta")

    class Meta:
        verbose_name = "Tipo de Oferta"
        verbose_name_plural = "Tipos de Ofertas"

    def __str__(self):
        return self.oferta_tipo

    def get_absolute_url(self):
        return reverse_lazy('donante_edit', kwargs={'pk': self.id})


class Donante(models.Model):
    """ Datos de los Donantes a utilizar
    """
    nombre = models.CharField(max_length=125, verbose_name="Nombre del Donante")
    pagina_web = models.URLField(verbose_name="Pagina Web",  blank=True)
    direccion = models.CharField(null=True, blank=True, max_length=150, verbose_name="Dirección")
    fax = models.IntegerField(verbose_name="Fax", null=True, blank=True)
    referido = models.CharField(max_length=70, verbose_name="Referido", null=True, blank=True)
    comentario = models.TextField(verbose_name="Comentario", null=True, blank=True)
    tipo_donante = models.ForeignKey(DonanteTipo, on_delete=models.PROTECT)
    nit = models.CharField(max_length=15, verbose_name="Numero de Nit", null=True, blank=True)

    class Meta:
        verbose_name = "Donante"
        verbose_name_plural = "Donantes"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('donante_detail', kwargs={'pk': self.id})


class Oferta(models.Model):
    """Datos de la oferta que se utilizaran
    """
    fecha_inicio = models.DateField(default=timezone.now().date(), verbose_name="Fecha de Contacto")
    fecha_bodega = models.DateField(
        verbose_name="Fecha de Ingreso a Bodega",
        null=True,
        blank=True)
    fecha_carta = models.DateField(
        verbose_name="Fecha de Creación de Carta",
        null=True,
        blank=True)
    recibido_por = models.ForeignKey(
                                    User,
                                    on_delete=models.CASCADE,
                                    verbose_name="Recibido por",
                                    related_name="recibido",
                                    null=True,
                                    blank=True)
    recibo_contable = models.BooleanField(verbose_name="Se entrego Recibo Contable")
    tipo_oferta = models.ForeignKey(OfertaTipo, on_delete=models.CASCADE)
    donante = models.ForeignKey(Donante, on_delete=models.CASCADE, verbose_name="Donante", related_name='ofertas')

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"

    def __str__(self):
        return str(self.fecha_inicio)

    def get_absolute_url(self):
        return reverse_lazy('oferta_detail', kwargs={'pk': self.id})


class OfertaHistorico(models.Model):
    """ Seguimiento de los comentario historicos que se haran en cada oferta
    """
    comentario = models.TextField(null=True, blank=True, verbose_name="Historico de Ofertas")
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Histórico de Oferta"
        verbose_name_plural = "Históricos de Ofertas"

    def __str__(self):
        return str(self.oferta) + self.comentario[:15]


class DonanteContacto(models.Model):
    """ Contacto del donante
    """
    nombre = models.CharField(max_length=125, verbose_name='Nombre')
    donante = models.ForeignKey(Donante, on_delete=models.CASCADE, related_name='contactos')

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('donante_detail', kwargs={'pk': self.donante.id})


class TelefonoCrm(models.Model):
    """ Gestionamiento los numeros telefonicos de los contactos y donates
    """
    numero = models.IntegerField(verbose_name="Número Telefónico")
    codigo = models.IntegerField(null=True, blank=True, verbose_name="Código de País")
    area = models.IntegerField(null=True, blank=True, verbose_name="Código de Área")
    donante = models.ForeignKey(Donante, on_delete=models.CASCADE, null=True, related_name='telefonos')
    contacto = models.ForeignKey(DonanteContacto, on_delete=models.CASCADE, related_name='telefonos')

    class Meta:
        verbose_name = "Telefono"
        verbose_name_plural = "Telefonos"

    def __str__(self):
        return str(self.numero)

    def get_absolute_url(self):
        return reverse_lazy('donante_detail', kwargs={'pk': self.donante.id})


class MailCrm(models.Model):
    """  Gestionamiento los correos electronicos de los donantes y contactos
    """
    mail = models.EmailField(max_length=25, verbose_name="Correo Electrónico")
    contacto = models.ForeignKey(DonanteContacto, on_delete=models.CASCADE,related_name='correos')
    donante = models.ForeignKey(Donante, on_delete=models.CASCADE, null=True, related_name='correos')

    class Meta:
        verbose_name = "Correo  Electrónico"
        verbose_name_plural = "Correos Electrónicos"

    def __str__(self):
        return self.mail

    def get_absolute_url(self):
        return reverse_lazy('donante_detail', kwargs={'pk': self.donante.id})
