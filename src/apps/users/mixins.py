from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from apps.users.models import Perfil


class PublicPerfilMixin(object):
    queryset = Perfil.objects.filter(public=True)


class CurrentUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.perfil.id is not self.get_object().id:
            raise PermissionDenied
        return super(CurrentUserMixin, self).dispatch(request, *args, **kwargs)


class AuthRequiredMixin(object):
    login_url = settings.LOGIN_URL

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path(), self.login_url)
        return super(AuthRequiredMixin, self).dispatch(request, *args, **kwargs)
