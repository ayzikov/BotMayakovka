import json
import os

from random import choice
from dotenv import load_dotenv

from aiohttp import ClientSession


async def action(tg_id: int, full_name: str, username: str, btn_name: str):
    '''
    Функция вызывается когда пользователь нажимает на любую кнопку в боте
    :param btn_name: название нажатой кнопки
    :return:
    '''

    # из БД запришиваются id всех пользователей и если id этого пользователя не присутствует в БД, то создается новый пользователь



    # если пользователь уже был, то обновляем ему last_time

    # сюда передается id пользователя, id сообщения и название кнопки
    # оно уходит во вьюхи
    # получаем из БД объект пользователя и создаем новый объект Action