from dynamic_preferences.types import BooleanPreference, StringPreference, Section, ChoicePreference
from dynamic_preferences.registries import user_preferences_registry, global_preferences_registry

ui = Section('ui')

@user_preferences_registry.register
class ThemeSkin(ChoicePreference):
	verbose_name = "Tema de interfaz"
	choices = (
		("skin-blue", "Azul"),
		("skin-blue-light", "Azul-blanco"),
		("skin-black-light", "Blanco"),
		("skin-black", "Blanco-negro"),
		("skin-red", "Rojo"),
		("skin-red-light", "Rojo-blanco"),
		("skin-green", "Verde"),
		("skin-green-light", "Verde-blanco"),
		("skin-yellow", "Amarillo"),
		("skin-yellow-light", "Amarillo-blanco"),
		("skin-purple", "Morado"),
		("skin-purple-light", "Morado-blanco"),
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