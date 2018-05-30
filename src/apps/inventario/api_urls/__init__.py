from .entrada import entrada_urlpatterns
from .desecho import desecho_urlpatterns


urlpatterns = desecho_urlpatterns + entrada_urlpatterns
