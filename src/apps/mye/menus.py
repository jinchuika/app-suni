from django.core.urlresolvers import reverse, reverse_lazy, resolve
from menu import Menu, MenuItem
from apps.main.menus import ViewMenuItem

#Administración
mye_children = (
	ViewMenuItem("Cooperantes",
		reverse_lazy("cooperante_list"),
		weight=10,
		icon="fa-users"),
	ViewMenuItem("Proyectos",
		reverse_lazy("proyecto_list"),
		weight=10,
		icon="fa-object-group"),
	)

Menu.add_item("user", ViewMenuItem("Monitoreo",
	'#',
	weight=10,
	icon="fa-search",
	children=mye_children))