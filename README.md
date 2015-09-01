# game-dictionary
Juego de adivinar el significado de palabras en español


## Instalación
Instrucciones para instalar un entorno virtual y el código necesario para la aplicación (también base de datos):

```
$ makevirtualenv game-dictionary
$ workon game-dictionary
$ cdvirtualenv
$ git clone https://github.com/jgsogo/game-dictionary.git
$ cd game-dictionary
$ pip install -r requirements.txt
$ cd dictionary_game
$ python manage.py migrate
```

## Apicultur
Ahora tienes que crear un archivo `secret.py` en el mismo directorio que está `settings.py` con el siguiente contenido:

```python
ACCESS_TOKEN_IO = '<aqui el access_token obtenido en https://apicultur.io/>'
ACCESS_TOKEN_STORE = '<aqui el access_token obtenido en https://store.apicultur.com/>'
```

Además tendrás que suscribirte a estos dos servicios:

 * [WordsbyFreq_Word_Molino_es - 1.0.0](http://apicultur.io/apis/info?name=WordsbyFreq_Word_Molino_es&version=1.0.0&provider=MolinodeIdeas)
 * [DiccionariodeEspanol - 1.0.0](https://store.apicultur.com/apis/info?name=DiccionariodeEspanol&version=1.0.0&provider=MolinodeIdeas)


## Ejecutar

```
$ python manage.py runserver
```

Y ahora ya puedes acceder a [http://localhost:8000/game/0/play/](http://localhost:8000/game/0/play/) y empezar a probarlo ;D

**NOTA.-** En cada llamada se realizan las consultas necesarias a las APIs, esto puede conllevar unos tiempos de espera
apreciables.


## TODO List
 * Aunque las vistas están preparadas para ser accedidas vía AJAX, no hay interfaz javascript programada.