from django.core.urlresolvers import reverse_lazy
from menu import Menu
from apps.main.menus import ViewMenuItem

# Nación Digital
ie_children = (
    ViewMenuItem(
        "Informe laboratorios",
        reverse_lazy("laboratorio_informe"),
        weight=10,
        icon="fa-desktop"),
    ViewMenuItem(
        "Informe validaciones",
        reverse_lazy("ie_validacion_informe"),
        weight=10,
        icon="fa-check"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Nación digital",
        '#',
        weight=40,
        icon="fa-cubes",
        group="nacion_digital",
        children=ie_children))

ie_admin = (
    ViewMenuItem(
        "Versiones de validación",
        reverse_lazy("ie_versionvalidacion_add"),
        weight=10,
        icon="fa-list"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Admin ND",
        '#',
        weight=40,
        icon="fa-gears",
        group="nacion_digital_admin",
        children=ie_admin))
