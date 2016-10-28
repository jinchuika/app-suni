SUNI2
=====
de [Fundación Sergio Paiz Andrade](http://funsepa.org/)

### Sistema Unificado de Información

Sistema encargado de gestionar toda la información relacionada con las operaciones de la [Funsepa](http://funsepa.org/).

## Dependencias

- Python 3
- pip
- Django 1.10
- MySQL
- virtualenv

## Instalación

#### Obtener el código
Clonar este repositorio:
```
git clone https://github.com/jinchuika/app-suni.git
```

#### Preparar el entorno
Entrar a la carpeta del repositorio (`cd app-suni`) y crear una carpeta llamada `etc`. En esa carpeta, crear un ambiente virtual con `virtualenv` llamado `venv`
```
virtualenv venv --no-site-packages --distribute
```
Activar el ambiente virtual con
```
source venv/bin/activate
```

#### Instalar dependencias de Python
Regresar a la carpeta raíz (`app-suni`) y instalar las dependencias con pip
```
pip install -r requirements.txt
```

#### Ejecutar el servidor
Ejecutar el servidor con el archivo manage.py desde la raíz.
```
python3 src/manage.py runserver 0.0.0.0:8000
```

#### Ejecutar el servidor dev
Ejecutar el servidor con el archivo manage.py desde la raíz.
```
python3 src/manage.py runserver 0.0.0.0:8000 --settings=src.settings_dev
=======
#### Ejecutar el servidor con la base de datos en
Escribir esto en settings_dev.py
```
Cambiar la raíz en
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

## Estructura del sistema
De forma ideal, las carpetas del sistema se verán así

```
.
├── etc
│   ├── media
│   └── venv
├── src
│   ├── apps
│   ├── fix
│   ├── src
│   ├── static
│   ├── templates
│   └── manage.py
├── README.md
└── requirements.txt
```
