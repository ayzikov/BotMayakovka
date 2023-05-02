import json
import os

from random import choice
from dotenv import load_dotenv

from aiohttp import ClientSession
from aiogram.types import FSInputFile

load_dotenv()
url = os.getenv('URL')

async def get_pieces_sort(sort_by: str = None, genre: str = None):
    '''
    Функция в зависимости от полученных параметров возвращает разные данные
    :param sort_by: по какому принципу происходит сортировка
    :param genre: если сортирова по жанру, то указывается жанр
    :return:
    '''

    data = {'sort_by': sort_by, 'genre': genre}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/pieces_sort/', data=json_data) as response:

            response = await response.json()
            return [{'name': dict_piece['name'], 'id': dict_piece['id']} for dict_piece in response]


async def piece_info_by_id(id_piece):
    '''
    :param id_piece: id пьесы
    :return: возвращает словарь с всей информацией о пьесе
    '''
    data = {'id_piece': id_piece}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/pieces_info/', data=json_data) as response:

            response = await response.json()
            return response[0]


async def piece_img_by_id(id_piece):
    '''
    :param id_piece: id пьесы
    :return: Функция возвращает объект FSInputFile, содержащий путь к изображению
    '''
    data = {'id_piece': id_piece}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/pieces_img/', data=json_data) as response:

            image_path = await response.json()
            img = FSInputFile(image_path)
            return img


async def get_random_piece():
    list_pieces = await get_pieces_sort(sort_by='name')
    id_piece = choice(list_pieces)['id']
    print(id_piece)
    return id_piece


