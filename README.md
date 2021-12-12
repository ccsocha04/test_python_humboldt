# Prueba Técnica - Instituto Humboldt 

Implementación de una REST API "Bored and Joke API" que expone los siguientes endpoints:

`GET /{tipo}`: Endpoint GET que recibe una palabra y retorna un objeto json con los atributos actividad y chiste.
`GET /data`: Endpoint GET que permite descargar la bitácora del servicio en formato csv, json, xlsx, txt. 

# Componentes

** Python >=3.7
** Pandas
** Django Rest Framework
** Base de Datos PostgreSQL >12
** Swagger UI
** BoredAPI
** JokeAPI
** Heroku

# Observaciones

1. Para la búsqueda del chiste con alguna de las palabras de `activity` se utilizaron las `stopwords` de `spacy`.
2. Durante la implemtanción del servicio de data se notó un posible bug si el `chiste` contenía comas, por tanto se reemplazaron.
3. En el endpoint `GET /data` es posible descargar en otros formatos, pero es necesario copiar el request en el navegador (o cliente).
4. No se configuro un acceso de base de datos en SQLite para mantener el mismo ambiente de desarrollo y producción. 

# Despligue

Configurar el ambiente de python en la IDE que se este utilizando.

```cmd
python -m venv .venv
cd /.venv/Scripts/activate.bat
```
Configurar el acceso a la base de datos en PostgreSQL en el archivo `local.py`

```python
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'test_humboldt'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'admin'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Una vez lo tengas clonado en tu repositori local y adicionalmente tengas el interprete de python activado,
debes ejecutar el siguiente comando:
```cmd
pip install requirements.txt
```
para correr en local recuerda que debes tener la base de datos en postgres ya activada.
```cmd
python manage.py migrate
python manage.py runserver
```
y navegas a la url: http://localhost:8000/api/ o a la que diga el comando.


* Es necesario configurar variables de entorno debido a que en en humbolt.