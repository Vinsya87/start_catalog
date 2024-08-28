from django.views.generic.base import ContextMixin
from users.forms import UserRegistrationForm


class RegistrForm(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = UserRegistrationForm
        return context
