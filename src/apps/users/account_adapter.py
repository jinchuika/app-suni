from allauth.account.adapter import DefaultAccountAdapter
from dynamic_preferences.registries import global_preferences_registry

class NoNewUsersAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """
        Evita que se creen nuevos usuarios
        """
        global_preferences = global_preferences_registry.manager()
        return global_preferences['admin__registro_usuarios']