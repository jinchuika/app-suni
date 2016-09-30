from django.core.urlresolvers import reverse, reverse_lazy
from menu import Menu, MenuItem
from apps.users import views

Menu.add_item("main", MenuItem("Tools",
	'perfil_list',
	weight=10,
	icon="tools"))

Menu.add_item("main", MenuItem("Reports",
	"perfil_list",
	weight=20,
	icon="report"))

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
	MenuItem("Equipo",
		reverse("kardex_equipo"),
		weight=10,
		icon="user"),
	MenuItem("Entradas",
		reverse("kardex_entrada"),
		weight=80,
		separator=True),
	MenuItem("Salidas",
		reverse("kardex_salida"),
		weight=90,
		separator=True,
		icon="fa fa-link"),
	)

Menu.add_item("user", MenuItem(
	"Kardex",
	reverse('kardex_equipo'),
	weight=10,
	children=kardex_children))