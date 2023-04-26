import json

import bot

from aiohttp import ClientSession
from aiogram.types import FSInputFile

from CBFactories import CBF_Pieces
from aiogram.filters.callback_data import CallbackQuery
from aiogram.fsm.context import FSMContext


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


async def back_button_with_img(query: CallbackQuery, callback_data: CBF_Pieces, state: FSMContext, action):
    '''Функция проверяет какой запрос был у пользователя по темам (алфавит, жанр, дата и тд.)
    и вызывает соответствующую функцию из bot.py'''

    if action == 'alphabet':
        await bot.get_alphabet_pieces(query, callback_data, state)
    elif action == 'date':
        await bot.get_date_pieces(query, callback_data, state)
    elif action == 'genre':
        await bot.get_genre_pieces(query, callback_data, state)
    elif action == 'non_popular':
        await bot.get_non_popular_pieces(query, callback_data, state)
    elif action == 'random':
        await bot.get_random_piece(query, callback_data, state)
    else:
        print(action)
