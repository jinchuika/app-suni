"""Este archivo se encarga de unificar los `urlpatterns` de las diferentes secciones del app.
En caso de que fuera creado un nuevo archivo de urls, debe ser incluido de la forma

```
from .archivo import urlpatterns as archivo_urls
```

y luego debe ser "incluido" en el `urlpatterns` del app
"""
from django.conf.urls import url, include

from .dispositivo import urlpatterns as dispositivo_urls
from .entrada import urlpatterns as entrada_urls
from .software import software_urls
from .bodega import urlpatterns as bodega_urls
from .desecho import urlpatterns as desecho_urls
from .salida import urlpatterns as salida_urls
from .repuesto import urlpatterns as repuesto_urls
from .prestamo import urlpatterns as prestamo_urls
from .interno import urlpatterns as interno_urls

urlpatterns = list(
    dispositivo_urls +
    entrada_urls +
    software_urls +
    bodega_urls +
    desecho_urls +
    salida_urls +
    repuesto_urls +
    prestamo_urls +
    interno_urls
)

urlpatterns.append(
    url(r'^api/', include(('apps.inventario.api_urls', 'inventario'), namespace='inventario_api')),
)
