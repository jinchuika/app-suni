from django.conf.urls import url
from apps.main import views as main_views

urlpatterns = [
    url(r'^', main_views.IndexView.as_view(), name="index"),
]
