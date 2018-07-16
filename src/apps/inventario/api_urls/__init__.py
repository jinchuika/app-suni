from .entrada import entrada_urlpatterns
from .desecho import desecho_urlpatterns
from .bodega import bodega_urlpatterns
from .dispositivo import dispositivo_urlpatterns
from .salida import salida_urlpatterns


urlpatterns = list(
    desecho_urlpatterns +
    entrada_urlpatterns +
    bodega_urlpatterns +
    dispositivo_urlpatterns +
    salida_urlpatterns
)
