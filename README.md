# Prueba Técnica - Instituto Humboldt 

Implementación de una REST API "Bored and Joke API" que expone los siguientes endpoints:

1. `GET /{tipo}`: Endpoint GET que recibe una palabra y retorna un objeto json con los atributos actividad y chiste.
2. `GET /data`: Endpoint GET que permite descargar la bitácora del servicio en formato csv, json, xlsx, txt. 

# Componentes

* Python >=3.7
* Pandas
* Django Rest Framework
* Base de Datos PostgreSQL >12
* Swagger UI
* BoredAPI
* JokeAPI
* Heroku

# Observaciones

1. Para la búsqueda del chiste con alguna de las palabras de `activity` se utilizaron las `stopwords` de `spacy`.
2. Durante la implemtanción del servicio de data se notó un posible bug si el `chiste` contenía comas, por tanto se reemplazaron.
3. En el endpoint `GET /data` es posible descargar en otros formatos, pero es necesario copiar el request en el navegador (o cliente).
4. No se configuro un acceso de base de datos en SQLite para mantener el mismo ambiente de desarrollo y producción. 

# Despligue REST API "Bored and Joke API"

Se descirbe una serie de pasos para realizar el respectivo despliegué de la REST API "Bored and Joke API"

## Instalar y configurar software 

* Es necesario instalar `Python` y configurar el ambiente en la IDE que se este utilizando, p.e. `Visual Studio Code`.

```cmd
python -m venv .venv
cd /.venv/Scripts/activate.bat
```

* Es necesario instalar el `PostgreSQL` y configurar el acceso a la base de datos en desde la aplicación en el archivo `local.py`

```python
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'test_humboldt'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '****'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
## Instalar requerimientos

Generar una copia del repositorio de la aplicación e instalar los requerimientos.

```git
git clone https://github.com/ccsocha04/test_python_humboldt.git
```
* Para instalar los requerimientos de Python se debe ejecutar el siguiente comando desde la carpeta del proyecto:

```cmd
pip install requirements.txt
```

* Para desplegar la REST API "Bored and Joke" localmente recuerda que debes tener la base de datos en postgres ya activada y ejecutar el siguiente comando:

```cmd
python manage.py migrate
python manage.py runserver
```
Finalmente, navegas a la url: http://localhost:8000/api/ o a la que diga el comando.