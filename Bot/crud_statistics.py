import json
import os

from random import choice
from dotenv import load_dotenv

from aiohttp import ClientSession


async def action(tg_id: int, full_name: str, username: str, msg_name: str, msg_id: int):
    '''
    Функция вызывается когда пользователь нажимает на любую кнопку в боте
    :param tg_id: id пользователя
    :param full_name: полное имя
    :param username: юзернейм
    :param msg_name: название кнопки на которую нажал пользователь
    :param msg_id: id сообщения
    :return:
    '''

    # из БД запришиваются id всех пользователей и если id этого пользователя не присутствует в БД, то создается новый пользователь
    # запрос возвращает True если пользователь существует и False в противном случае

    data = {'tg_id': tg_id, 'full_name': full_name, 'username': username}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/user/', data=json_data) as response:

            print(response)


    # если пользователь уже был, то обновляем ему last_time
    data = {'tg_id': tg_id}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.put('http://127.0.0.1:8000/user/', data=json_data) as response:

            print(response)


    # сюда передается id пользователя, id сообщения и название кнопки
    # оно уходит во вьюхи
    # получаем из БД объект пользователя и создаем новый объект Action
    data = {'tg_id': tg_id, 'msg_name': msg_name, 'msg_id': msg_id}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.post('http://127.0.0.1:8000/action/', data=json_data) as response:

            print(response)


async def statistic(message, msg_name):
    await action(tg_id=message.from_user.id,
                 full_name=message.from_user.full_name,
                 username=message.from_user.username if message.from_user.username else '',
                 msg_id=message.message_id,
                 msg_name=msg_name)


async def get_statistics(users: str, actions: str, comands: str):
    data = {'users': users, 'actions': actions, 'comands': comands}
    json_data = json.dumps(data)
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/statistics/', data=json_data) as response:

            response = await response.json()
            return response