from django.shortcuts import redirect
from django.views.generic.base import ContextMixin
from apps.escuela.forms import ContactoTelefonoFormSet, ContactoMailFormSet


class ContactoContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(ContactoContextMixin, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        return {
            'telefono': ContactoTelefonoFormSet(
                self.request.POST or None,
                instance=self.object),
            'mail': ContactoMailFormSet(
                self.request.POST or None,
                instance=self.object),
        }

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        instance = form.save()
        for nombre, formset in named_formsets.items():
            if formset.is_valid():
                for form in formset.forms:
                    item = form.save(commit=False)
                    print(item)
                    item.contacto = instance
                    item.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))
        return redirect(self.get_success_url())
