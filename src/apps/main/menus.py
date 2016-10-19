from django.core.urlresolvers import reverse_lazy
from menu import Menu, MenuItem


class ViewMenuItem(MenuItem):
    def __init__(self, *args, **kwargs):
        super(ViewMenuItem, self).__init__(*args, **kwargs)
        if 'perm' in kwargs:
            self.perm = kwargs.pop('perm')

            def check(self, request):
                """Revisa los permisos"""
                is_visible = True
                if hasattr(self, 'perm'):
                    if request.user.has_perm(self.perm):
                        is_visible = True
                    else:
                        is_visible = False
                        self.visible = is_visible


# Administración
admin_children = (
    ViewMenuItem(
        "Lista de perfiles",
        reverse_lazy("perfil_list"),
        weight=10,
        icon="fa-users"),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Administración",
        reverse_lazy("perfil_list"),
        weight=10,
        icon="fa-key",
        children=admin_children))
