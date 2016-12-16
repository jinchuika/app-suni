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
        for name, f in named_formsets.items():
            if f.is_valid():
                f.save()
            else:
                return self.render_to_response(self.get_context_data(form=form))
        return redirect(self.get_success_url())

        if not all((x.is_valid() for x in named_formsets.values())):
            print("error")
            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))
        else:
            self.object = form.save()
        for name, formset in named_formsets.items():
            formset.save()
        return redirect(self.get_success_url())
