from django.core.urlresolvers import reverse, reverse_lazy, resolve
from menu import Menu, MenuItem


class ViewMenuItem(MenuItem):
	def __init__(self, *args, **kwargs):
		super(ViewMenuItem, self).__init__(*args, **kwargs)
		if 'perm' in kwargs:
			self.perm = kwargs.pop('perm')

	def check(self, request):
		"""Check permissions based on our view"""
		is_visible = True
		#match = resolve(self.url)
		if hasattr(self, 'perm'):
			if request.user.has_perm(self.perm):
				is_visible = True
			else:
				is_visible = False
		self.visible = is_visible


#Administración
admin_children = (
	ViewMenuItem("Lista de perfiles",
		reverse_lazy("perfil_list"),
		weight=10,
		icon="fa-users"),
	)

Menu.add_item("user", ViewMenuItem("Administración",
	reverse_lazy("perfil_list"),
	weight=10,
	icon="fa-key",
	children=admin_children))



#Kardex
kardex_children = (
	ViewMenuItem("Equipo",
		reverse_lazy("kardex_equipo"),
		weight=10,
		icon="fa-desktop"),
	ViewMenuItem("Entradas",
		reverse_lazy("kardex_entrada"),
		weight=20,
		icon='fa-arrow-up'),
	ViewMenuItem("Salidas",
		reverse_lazy("kardex_salida"),
		weight=30,
		icon="fa-arrow-down"),
	ViewMenuItem("Proveedores",
		reverse_lazy("kardex_proveedor"),
		weight=40,
		icon="fa-truck"),
	)

Menu.add_item("user", ViewMenuItem("Kardex",
	reverse('kardex_equipo'),
	weight=20,
	icon="fa-cog",
	children=kardex_children))


# Escuelas
escuela_children = (
	ViewMenuItem("Crear escuela",
		reverse_lazy("escuela_add"),
		weight=10,
		icon="fa-plus-square-o",
		perm='escuela.add_escuela'),
	)

Menu.add_item("user", ViewMenuItem(
	"Escuelas",
	'#',
	weight=10,
	icon="fa-building-o",
	children=escuela_children))

# --- CONTACTOS FUNDRAISINGS --- #
contacto_children = (
	ViewMenuItem("Contactos",
		reverse_lazy("contacto_contactos"),
		weight=10,
		icon="fa-user"),
	ViewMenuItem("Empresa",
		reverse_lazy("contacto_empresa"),
		weight=20,
		icon='fa-building-o'),
	ViewMenuItem("Evento",
		reverse_lazy("contacto_evento"),
		weight=30,
		icon="fa-calendar"),
	)

Menu.add_item("user", ViewMenuItem("Directorio",
	reverse('contacto_contactos'),
	weight=20,
	icon="fa-users",
	children=contacto_children))