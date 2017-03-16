from django.http import JsonResponse
from django.views.generic.edit import FormView
from braces.views import LoginRequiredMixin, CsrfExemptMixin


class InformeMixin(CsrfExemptMixin, LoginRequiredMixin, FormView):
    form_class = None
    template_name = ''

    def get_queryset(self, filtros):
        return []

    def create_response(self, queryset):
        return []

    def post(self, request, *args, **kwargs):
        item_list = self.get_queryset(self.request.POST)
        return JsonResponse(self.create_response(item_list), safe=False)
