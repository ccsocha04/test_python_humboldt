import requests
import random

from rest_framework import status, serializers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_pandas import PandasView

from bored_and_joke.serializers import BoredAndJokeForGetSerializer, BoredAndJokeForCSVSerializer
from bored_and_joke.models import BoredAndJoke
from rest_framework_csv import renderers as r

from .custom_errors import IncorrectType, ThirdPartyAPIError
from .stops_ import spacy_stop_words


class BoredAndJokeView(APIView):
    def get(self, request, tipo: str):
        try:
            self.check_type(tipo)
            bored_api_data = self.check_third_party_api(word=tipo, api='bored', message='Error en la API de Bored')
            bored_and_joke = self.obtain_bored_data(bored_api_data, tipo)

            # Para borrar los stopwords
            search_word = [word.lower() for word in bored_api_data['activity'].split()
                           if word.lower() not in spacy_stop_words]
            random_word = random.choice(search_word)
            search_word.remove(random_word)

            joke_api_response = self.check_third_party_api(
                word=random_word, api='joke', message='Error en la API de Joke')
            bored_and_joke['chiste'] = self.check_joke(joke_api_response, search_word)
            serializer = BoredAndJokeForGetSerializer(data=bored_and_joke)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IncorrectType as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ThirdPartyAPIError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def check_type(self, tipo: str):
        allowed_types = ["education", "recreational", "social", "diy",
                         "charity", "cooking", "relaxation", "music", "busywork"]
        if tipo not in allowed_types:
            raise IncorrectType("El tipo no es permitido")

    def check_third_party_api(self,  word: str, api: str, message: str) -> dict:
        """Comprueba que la API de Bored y Joke est?? funcionando y retorna un diccionario
        con la respuesta json"""
        if api == 'bored':
            url = f'https://www.boredapi.com/api/activity?type={word}'
        else:
            url = f'https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw&contains={word}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ThirdPartyAPIError(message)
        return response.json()

    def obtain_bored_data(self, request_json: dict, tipo: str) -> dict:
        """Obtener los par??metros que ser??n utilizados en el serializador"""
        request_json = {
            'type': tipo,
            'actividad': request_json['activity'].replace(',', ''),
            'key': request_json['key']
        }
        return request_json

    def check_joke(self, response, word_list: list):
        """Comprueba la l??gica solicitada de la api de Joke.
        # TODO deber??a usarse una funci??n para evitar doble chequeo de ['error'] is True"""
        if response['error'] is True:
            response = self.check_third_party_api(word=random.choice(word_list),
                                                  api='joke',
                                                  message='Error en la API de Joke')
            if response['error'] is True:
                return 'No se encontr?? un chiste.'

        if response['type'] == 'twopart':
            joke = response['setup'] + '->' + response['delivery']
        else:
            joke = response['joke']
        return joke.replace(',', '')


class PandasBoredJokeView(PandasView):
    queryset = BoredAndJoke.objects.all()
    serializer_class = BoredAndJokeForCSVSerializer




