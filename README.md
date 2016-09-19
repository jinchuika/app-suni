SUNI2
=====
de [Fundación Sergio Paiz Andrade](http://funsepa.org/)

### Sistema Unificado de Información

Sistema encargado de gestionar toda la información relacionada con las operaciones de la [Funsepa](http://funsepa.org/).

## Instalación
Es necesario tener instalado el gestor de paquetes pip.

Crear un ambiente virtual

```
virtualenv venv --no-site-packages --distribute
```


Instalar los requerimientos
```
pip install -r requirements.txt
```

Activar el ambiente virtual con
```
source venv/bin/activate
```

Ejecutar el servidor desde el archivo manage.py.
```
python3 src/manage.py runserver
```
