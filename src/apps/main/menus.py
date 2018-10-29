from menu import MenuItem
from django.contrib.auth.models import Permission

class ViewMenuItem(MenuItem):
    def __init__(self, *args, **kwargs):
        super(ViewMenuItem, self).__init__(*args, **kwargs)
        if 'perm' in kwargs:
            self.perm = kwargs.pop('perm')
        if 'test' in kwargs:
            self.test = kwargs.pop('test')

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

        if hasattr(self, 'test'):
            self.visible = self.test(request.user)
