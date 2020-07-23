from django.contrib import admin
from django.apps import apps
for model in apps.get_app_config('coursera').models.values():
    admin.site.register(model)

# Register your models here.