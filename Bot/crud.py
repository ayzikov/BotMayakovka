import json

from aiohttp import ClientSession
from aiogram.types import FSInputFile


async def get_pieces(sort_by: str = None, genre: str = None, id: int = None, random: bool = False):
    '''
    Функция в зависимости от полученных параметров возвращает разные данные
    :param sort_by: по какому принципу происходит сортировка
    :param genre: если сортирова по жанру, то указывается жанр
    :param name: если указано имя, то возвращается данные по имени пьесы
    :param random: если True, то возвращается рандомное имя пьесы
    :return:
    '''

    data = {'sort_by': sort_by, 'genre': genre, 'id': id, 'random': random}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/pieces/', data=json_data) as response:

            response = await response.json()
            if random:
                return {'name': response['name'], 'id': response['id']}
            elif not id:
                return [{'name': dict_piece['name'], 'id': dict_piece['id']} for dict_piece in response]

async def get_piece_name_by_id(id: int):
    data = {'id': id}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/pieces/', data=json_data) as response:

            response = await response.json()
            return response[0]['name']


async def get_piece_description_by_id(id: int):
    data = {'id': id, 'description': True}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/pieces/', data=json_data) as response:

            response = await response.json()
            return response[0]


async def get_piece_img_by_id(id: int):
    data = {'id': id, 'image': True}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/pieces/', data=json_data) as response:

            image_path = await response.json()
            img = FSInputFile(image_path)
            return img
