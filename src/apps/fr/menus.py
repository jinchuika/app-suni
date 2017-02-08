from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# --- CONTACTOS FUNDRAISINGS --- #
contacto_children = (
    ViewMenuItem(
        "Contactos",
        reverse_lazy("contacto_contactos"),
        weight=10,
        icon="fa-user"),
    ViewMenuItem(
        "Empresa",
        reverse_lazy("contacto_empresa"),
        weight=20,
        icon='fa-building-o'),
    ViewMenuItem(
        "Evento",
        reverse_lazy("contacto_evento"),
        weight=30,
        icon="fa-calendar"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Directorio",
        reverse_lazy('contacto_contactos'),
        weight=40,
        icon="fa-users",
        group="fr",
        children=contacto_children))
