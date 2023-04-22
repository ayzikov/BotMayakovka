from aiohttp import ClientSession
import json
from random import choice


async def get_pieces(sort_by: str = None, genre: str = None, name: str = None, random: bool = False):
    '''
    Функция в зависимости от полученных параметров возвращает разные данные
    :param sort_by: по какому принципу происходит сортировка
    :param genre: если сортирова по жанру, то указывается жанр
    :param name: если указано имя, то возвращается данные по имени пьесы
    :param random: если True, то возвращается рандомное имя пьесы
    :return:
    '''

    data = {'sort_by': sort_by, 'genre': genre, 'name': name, 'random': random}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/pieces/', data=json_data) as response:

            response = await response.json()
            if random:
                return response['name']
            elif not name:
                return [dict_piece['name'] for dict_piece in response]
            else:
                return response[0]['description_piece']
