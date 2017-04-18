from datetime import datetime, timedelta
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin
from apps.tpe.models import Garantia


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['widgets'] = {}
        if self.request.user.groups.filter(name='garantia').exists():
            context['widgets']['prox_garantia'] = Garantia.objects.filter(
                fecha_vencimiento__gte=datetime.now(),
                fecha_vencimiento__lte=(datetime.now() + timedelta(days=7)))
        return context
