from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from menu import Menu
from apps.main.menus import ViewMenuItem

#Entradas
recaudacion_children = (
    ViewMenuItem(
        "Entrada",
        reverse_lazy("recaudacion_entrada_add"),
        weight=12,
        icon="fa-pencil-square-o"
    ),
    ViewMenuItem(
        "Proveedores",
        reverse_lazy("recaudacion_proveedor_detail"),
        weight=12,
        icon="fa-address-book-o"
    ),
     ViewMenuItem(
        "Articulos",
        reverse_lazy("recaudacion_articulo_add"),
        weight=12,
        icon="fa-shopping-bag"
    ),
    ViewMenuItem(
        "Salida",
        reverse_lazy("recaudacion_salida_add"),
        weight=12,
        icon="fa-sign-out"
    )
)
Menu.add_item(
    "user",
    ViewMenuItem(
        "Recaudacion",
        reverse_lazy('recaudacion_entrada_add'),
        weight=10,
        icon="fa-usd",
        group="recaudacion",
        children=recaudacion_children
    )
)
