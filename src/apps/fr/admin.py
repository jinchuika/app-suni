from django.contrib import admin
from apps.fr.models import *
from django.apps import apps


for model in apps.get_app_config('fr').models.values():
	admin.site.register(model)
# Register your models here.
