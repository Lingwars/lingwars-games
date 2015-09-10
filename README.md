
Lingwars | Games
================

Proyecto web de la comunidad [Lingwars](http://lingwars.github.io/blog/) en el
que se proponen un conjunto de desafíos de temática lingüística. ¿Te atreves?


Pruebas/desarrollo
------------------

Si quieres ejecutarlo en tu ordenador puedes seguir estos pasos:

1. Clonar el repositorio
1. Instalar las dependencias correspondientes a tu version de Python:

   ```
   $ pip install requirements_py3
   ```

1. Necesitarás conseguir los `access_token` necesarios en Apicultur y
   guardarlos en un archivo `appweb/appweb/secret.py` (misma carpeta que `settings.py`)
1. Instalar la base de datos (por defecto utiliza `sqlite3`):

   ```
   $ python appweb/manage.py migrate
   ```

1. Arrancar un servidor local:

   ```
   $ python appweb/manage.py runserver
   ```

1. Y abrir en tu navegador la url http://localhost:8000/

... pero es mucho mejor jugar online y ver cómo evoluciona tu ranking.