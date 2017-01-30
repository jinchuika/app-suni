from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Administración
admin_children = (
    ViewMenuItem(
        "Lista de perfiles",
        reverse_lazy("perfil_list"),
        weight=91,
        icon="fa-users",
        perm='users.add_user'),
    ViewMenuItem(
        "Crear nuevo usuario",
        reverse_lazy("perfil_add"),
        weight=92,
        icon="fa-user",
        perm='users.add_user'),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Administración",
        reverse_lazy("perfil_list"),
        weight=90,
        icon="fa-key",
        children=admin_children,
        group='admin'))
