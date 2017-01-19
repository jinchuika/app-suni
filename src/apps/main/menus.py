from django.core.urlresolvers import reverse_lazy
from menu import Menu, MenuItem


class ViewMenuItem(MenuItem):
    def __init__(self, *args, **kwargs):
        super(ViewMenuItem, self).__init__(*args, **kwargs)
        if 'perm' in kwargs:
            self.perm = kwargs.pop('perm')

    def check(self, request):
        """ Revisa por grupo """
        if hasattr(self, 'group'):
            if request.user.groups.filter(name=self.group).exists():
                self.visible = True
                return True
            else:
                self.visible = False
        """ Revisa los permisos """
        if hasattr(self, 'perm'):
            if request.user.has_perm(self.perm):
                self.visible = True
                return True
            else:
                self.visible = False


# Administración
admin_children = (
    ViewMenuItem(
        "Lista de perfiles",
        reverse_lazy("perfil_list"),
        weight=10,
        icon="fa-users",
        perm='users.add_user'),)

Menu.add_item(
    "user",
    ViewMenuItem(
        "Administración",
        reverse_lazy("perfil_list"),
        weight=10,
        icon="fa-key",
        children=admin_children,
        group='admin'))
