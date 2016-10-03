from dynamic_preferences.types import BooleanPreference, StringPreference, Section, ChoicePreference
from dynamic_preferences.registries import user_preferences_registry, global_preferences_registry

ui = Section('ui')

@user_preferences_registry.register
class ThemeSkin(ChoicePreference):
	verbose_name = "Tema de interfaz"
	choices = (
		("skin-blue", "Azul"),
		("skin-black", "Negro"),
		("skin-red", "Rojo"),
		("skin-green", "Verde"),
		)
	section = "ui"
	name = "skin"
	default = "skin-blue"

@user_preferences_registry.register
class ThemeSkin(BooleanPreference):
	verbose_name = "Navegación estática"
	section = "ui"
	name = "fixed"
	default = False