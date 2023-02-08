"""Este archivo se encarga de unificar los `urlpatterns` de las diferentes secciones del app.
En caso de que fuera creado un nuevo archivo de urls, debe ser incluido de la forma

```
from .archivo import urlpatterns as archivo_urls
```

y luego debe ser "incluido" en el `urlpatterns` del app
"""
from django.conf.urls import url, include

from .entrada import urlpatterns as entrada_urls
from .dispositivo import urlpatterns as dispositivo_urls
from .salida import urlpatterns as salida_urls
urlpatterns = list(    
    entrada_urls +
    dispositivo_urls +
    salida_urls
)

urlpatterns.append(
    url(r'^api/', include(('apps.beqt.api_urls', 'beqt'), namespace='beqt_api')),
)
