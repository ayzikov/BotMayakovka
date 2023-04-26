import asyncio
import crud

from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, InlineKeyboardBuilder
from CBFactories import CBF_Pieces
async def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Хочу узнать про все пьесы'),
             KeyboardButton(text='Хочу пьесу под настроение')],
        ],
        resize_keyboard=True,
        one_time_keyboard=True)

    return markup

async def info_piece_inline_keyboard(id, random: bool = False):
    '''Если значение random передано и является True, то кнопка назад имеет другое значение value'''
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='О пьесе', callback_data=CBF_Pieces(action='about_piece',
                                                                         id=id).pack())
    btn2 = InlineKeyboardButton(text='О постановке', callback_data=CBF_Pieces(action='about_play',
                                                                              id=id).pack())

    if random:
        btn3 = InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='back',
                                                                           value='name').pack())
    else:
        btn3 = InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='back',
                                                                           value='state').pack())


    builder.add(btn1, btn2, btn3)
    builder.adjust(1)
    return builder.as_markup()
async def all_pieces_inline_keyboard():
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='По алфавиту', callback_data=CBF_Pieces(action='alphabet').pack())
    btn2 = InlineKeyboardButton(text='По дате выхода', callback_data=CBF_Pieces(action='date').pack())
    btn3 = InlineKeyboardButton(text='Случайная пьеса', callback_data=CBF_Pieces(action='random').pack())
    btn4 = InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='back',
                                                                       value='main_menu').pack())

    builder.add(btn1, btn2, btn3, btn4)
    builder.adjust(1)
    return builder.as_markup()



async def mood_pieces_inline_keyboard():
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='Комедии', callback_data=CBF_Pieces(action='genre',
                                                                         value='Комедия').pack())
    btn2 = InlineKeyboardButton(text='Драмы', callback_data=CBF_Pieces(action='genre',
                                                                        value='Драма').pack())
    btn3 = InlineKeyboardButton(text='Любой жанр, что-то незаезженное', callback_data=CBF_Pieces(action='non_popular').pack())
    btn4 = InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='back',
                                                                       value='main_menu').pack())

    builder.add(btn1, btn2, btn3, btn4)
    builder.adjust(1)
    return builder.as_markup()


async def sort_inline_keyboard(sort_by: str = None, genre: str = None):
    pieces_list = await crud.get_pieces(sort_by=sort_by, genre=genre)
    pieces_iterator = iter(pieces_list)

    builder = InlineKeyboardBuilder()

    while 1:
        try:
            itr = next(pieces_iterator)
            piece_name = itr['name']
            piece_id = itr['id']
        except:
            flag = False
            break

        builder.add(InlineKeyboardButton(text=piece_name, callback_data=CBF_Pieces(action='get_piece',
                                                                                   id=piece_id).pack()))

    builder.add(InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='back',
                                                                            value=sort_by).pack()))

    builder.adjust(1)
    return builder.as_markup()



async def about_piece_inline_keyboard():
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='Подробнее', callback_data=CBF_Pieces(action='more').pack())
    btn2 = InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='back',
                                                                       value='state_piece').pack())

    builder.add(btn1, btn2)
    builder.adjust(1)

    return builder.as_markup()

async def more_about_piece_inline_keyboard():
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='back',
                                                                       value='state_piece').pack())

    builder.add(btn1)
    builder.adjust(1)

    return builder.as_markup()


async def about_play_inline_keyboard():
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='Сходить на постановку', callback_data=CBF_Pieces(action='go_play').pack())
    btn2 = InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='back',
                                                                       value='state_piece').pack())

    builder.add(btn1, btn2)
    builder.adjust(1)

    return builder.as_markup()


async def go_to_the_play_inline_keyboard():
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='Назад', callback_data=CBF_Pieces(action='back',
                                                                       value='state_piece').pack())

    builder.add(btn1)
    return builder.as_markup()
