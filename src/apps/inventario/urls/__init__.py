"""Este archivo se encarga de unificar los `urlpatterns` de las diferentes secciones del app.
En caso de que fuera creado un nuevo archivo de urls, debe ser incluido de la forma

```
from .archivo import urlpatterns as archivo_urls
```

y luego debe ser "incluido" en el `urlpatterns` del app
"""

from .dispositivo import urlpatterns as dispositivo_urls
from .entrada import urlpatterns as entrada_urls
from .software import software_urls
from .bodega import urlpatterns as bodega_urls
from .desecho import urlpatterns as desecho_urls

urlpatterns = dispositivo_urls + entrada_urls + software_urls + bodega_urls + desecho_urls
