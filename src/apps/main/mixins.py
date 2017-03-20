from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.edit import FormView
from braces.views import LoginRequiredMixin, CsrfExemptMixin


class InformeMixin(CsrfExemptMixin, LoginRequiredMixin, FormView):
    form_class = None
    template_name = ''
    queryset = None
    filter_list = None

    def get_queryset(self, filtros):
        queryset = self.queryset
        filter_clauses = None
        for key, filtro in self.filter_list.items():
            if filtros.get(key):
                q = Q(**{"%s" % filtro: filtros.get(key)})
                if filter_clauses:
                    filter_clauses = filter_clauses & q
                else:
                    filter_clauses = q
        if filter_clauses:
            queryset = queryset.filter(filter_clauses)
        return queryset

    def create_response(self, queryset):
        return []

    def post(self, request, *args, **kwargs):
        item_list = self.get_queryset(self.request.POST)
        return JsonResponse(self.create_response(item_list), safe=False)
