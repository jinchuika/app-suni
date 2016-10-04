from django.core.urlresolvers import reverse, reverse_lazy
from menu import Menu, MenuItem
from apps.users import views

admin_children = (
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
	children=admin_children))

kardex_children = (
	MenuItem("Equipo",
		reverse("kardex_equipo"),
		weight=80,
		icon="user"),
	MenuItem("Entradas",
		reverse("kardex_entrada"),
		weight=10,
		icon="user"),
	MenuItem("Salidas",
		reverse("kardex_salida"),
		weight=20,
		icon="fa fa-link"),
	)

Menu.add_item("user", MenuItem(
	"Kardex",
	reverse('kardex_equipo'),
	weight=20,
	children=kardex_children))