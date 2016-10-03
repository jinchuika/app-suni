from django.core.urlresolvers import reverse, reverse_lazy, resolve
from menu import Menu, MenuItem
from apps.users import views

class ViewMenuItem(MenuItem):
	def __init__(self, *args, **kwargs):
		super(ViewMenuItem, self).__init__(*args, **kwargs)
		if 'perm' in kwargs:
			self.perm = kwargs.pop('perm')

	def check(self, request):
		"""Check permissions based on our view"""
		is_visible = True
		match = resolve(self.url)
		if hasattr(self, 'perm'):
			if request.user.has_perm(self.perm):
				is_visible = True
			else:
				is_visible = False
		self.visible = is_visible


myaccount_children = (
	MenuItem("Lista de perfiles",
		"perfil_list",
		weight=10,
		icon="user"),
	MenuItem("Mi Perfil",
		"profile",
		weight=80,
		separator=True),
	MenuItem("Logout",
		"login",
		weight=90,
		separator=True,
		icon="fa fa-link"),
	)


# Add a My Account item to our user menu
Menu.add_item("user", MenuItem("Administración",
	"index",
	weight=10,
	children=myaccount_children))

kardex_children = (
	ViewMenuItem("Equipo",
		reverse_lazy("kardex_equipo"),
		weight=10,
		icon="fa-desktop"),
	ViewMenuItem("Entradas",
		reverse_lazy("kardex_entrada"),
		weight=80,
		icon='fa-arrow-up'),
	ViewMenuItem("Salidas",
		reverse_lazy("kardex_salida"),
		weight=90,
		icon="fa-arrow-down"),
	)

Menu.add_item("user", MenuItem(
	"Kardex",
	reverse_lazy('kardex_equipo'),
	weight=10,
	icon="fa-cogs",
	children=kardex_children))


# KARDEX
escuela_children = (
	ViewMenuItem("Crear escuela",
		reverse_lazy("escuela_add"),
		weight=10,
		icon="user",
		perm='escuela.add_escuela'),
	)

Menu.add_item("user", MenuItem(
	"Escuelas",
	'#',
	weight=10,
	children=escuela_children))