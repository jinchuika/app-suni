from django.db import models
from apps.users.models import Perfil
from django.contrib.auth.models import Group
from mptt.models import MPTTModel, TreeForeignKey

class MenuPagina(MPTTModel):
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
	name = models.CharField(max_length=30, unique=True)
	url = models.CharField(max_length=50)
	active = models.BooleanField(default=False)
	titulo = models.CharField(max_length=100, null=True, blank=True)
	icon = models.CharField(max_length=25, null=True, blank=True)
	extra = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.name

	class MPTTMeta:
		order_insertion_by = ['name']

class MenuGrupo(models.Model):
	grupo = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='nav_menu')
	menu = models.ManyToManyField(MenuPagina)

	class Meta:
		verbose_name = 'Menú de grupo'
		verbose_name_plural = 'menús de grupos'

	def __str__(self):
		return "Menú de " + str(self.grupo)