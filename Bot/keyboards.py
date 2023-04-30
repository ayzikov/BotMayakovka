import asyncio
import crud

from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardBuilder, InlineKeyboardMarkup
from CBFactories import CBF_Pieces
from aiogram.fsm.context import FSMContext
async def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Хочу узнать про все пьесы')],
             [KeyboardButton(text='Хочу пьесу под настроение')]
        ],
        resize_keyboard=True,
        is_persistent=True)

    return markup


async def all_pieces_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='По алфавиту')],
            [KeyboardButton(text='По дате')],
            [KeyboardButton(text='Случайная пьеса')],
            [KeyboardButton(text='Главное меню')]
        ],
        resize_keyboard=True,
        is_persistent=True)

    return markup

async def mood_pieces_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Комедии')],
             [KeyboardButton(text='Драмы')],
             [KeyboardButton(text='Малоизвестные пьесы')],
             [KeyboardButton(text='Главное меню')]
             ],
        resize_keyboard=True,
        is_persistent=True)

    return markup


async def pieces_inline_keyboard(list_dicts_pieces, page: int = 1):

    '''
    Выводится инлайн клавиатура в которой первые 7 строк это пьесы, на 8 строке находятся кнопки
    с номерами страни
    Если пользователь выбрал отсортированные пьесы, то по умолчанию выводится первая страниа
    Если пользователь выбрал страницу, то она передается в эту функцию и выводится

    :param list_dicts_pieces: список со словарями. В каждом словаре содержится имя и id пьесы
    :param page: страница с пьесами
    :return: инлайн клавиатура
    '''

    list_dicts_pieces = list_dicts_pieces               # список со словарями. В каждом словаре содержится имя и id пьесы
    quantity_pages = len(list_dicts_pieces) // 7 + 1    # количество страниц с пьесами. На каждой странице находится по 7 пьес
    number_for_slice = (page - 1) * 7                   # число для вычислений среза списка со словарями
    builder = InlineKeyboardBuilder()

    # берется срез из списка со словарями, который определяется переданной в функцию страницей
    # создаются инлайн кнопки с названием каждой пьесы которые содержат ее id и добавляются в по одной на строку
    for piece_dict in list_dicts_pieces[number_for_slice: number_for_slice + 7]:
        builder.row(InlineKeyboardButton(text=piece_dict['name'], callback_data=CBF_Pieces(action='get_piece',
                                                                                           id_piece=piece_dict['id']).pack()))

    # создаются кнопки с номерами страниц
    # записываются в список чтобы вывести их на одной строке
    buttons_pages_numbers = []
    for page_number in range(1, quantity_pages + 1):
        buttons_pages_numbers.append(InlineKeyboardButton(text=page_number, callback_data=CBF_Pieces(action='page',
                                                                                                  page_number=page_number).pack()))

    builder.row(*buttons_pages_numbers) # добавляем инлайн кнопки с номерами страниц на одну строку


    return builder.as_markup()          # возвращаю разметку


async def info_piece_inline_keyboard():
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='Сюжет', callback_data=CBF_Pieces(action='detail').pack())
    btn2 = InlineKeyboardButton(text='О постановке', callback_data=CBF_Pieces(action='info_play').pack())

    builder.add(btn1, btn2)
    return builder.as_markup()

async def detailed_info_piece_inline_keyboard(id_piece):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='get_piece',
                                                                         id_piece=id_piece).pack()))
    return builder.as_markup()


async def about_play_piece_inline_keyboard(id_piece):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Сходить на постановку', callback_data=CBF_Pieces(action='go_play').pack()))
    builder.add(InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='get_piece',
                                                                         id_piece=id_piece).pack()))
    builder.adjust(1)
    return builder.as_markup()


async def go_play_piece_inline_keyboard(id_piece):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='get_piece',
                                                                            id_piece=id_piece).pack()))
    return builder.as_markup()