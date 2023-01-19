from .entrada import entrada_urlpatterns
from .dispositivo import dispositivo_urlpatterns


urlpatterns = list(
    entrada_urlpatterns +
    dispositivo_urlpatterns
)
