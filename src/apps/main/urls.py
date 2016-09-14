from django.conf.urls import url, include
from django.contrib import admin
from apps.main import views as main_views

urlpatterns = [
    url(r'^', main_views.index, name="index"),
]
