from django.contrib import admin
from .models import *
from django.apps import apps
from .forms import * 
# Register your models here.


#class AdminEquipo(admin.ModelAdmin):
#	form = FormularioEquipo



for model in apps.get_app_config('kardex').models.values():
   admin.site.register(model)


