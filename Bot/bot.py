# файлы проекта
import crud
import keyboards
import texts

from CBFactories import CBF_Pieces

# отдельные импорты
import logging
import asyncio
import os
from magic_filter import F
from dotenv import load_dotenv

# импорты aiogram
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackQuery



load_dotenv()

token = os.getenv('BOTTOKEN')

bot = Bot(token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Функция, которая будет вызываться при получении команды /start
@dp.message(Command(commands=['start']))
async def hello_message(message: Message):
    """
        Обработчик команды /start
        Отправляет пользователю приветственное сообщение и главное меню
    """
    # Получаем клавиатуру главного меню
    markup = await keyboards.main_menu_keyboard()

    # Получаем текст приветственного сообщения
    text = texts.hello_text

    await message.answer(text=text, reply_markup=markup)

@dp.message(Command(commands=['menu']))
async def main_menu(message: Message):
    """
        Обработчик команды /menu
        Отправляет пользователю главное меню
    """
    # Получаем клавиатуру главного меню
    markup = await keyboards.main_menu_keyboard()

    # Получаем текст главного меню
    text = texts.main_menu_text
    await message.answer(text=text, reply_markup=markup)


#ОБРАБОТКА КНОПОК ГЛАВНОГО МЕНЮ
@dp.message(Text(text='Хочу узнать про все пьесы'))
async def all_pieces(message: Message):
    markup = await keyboards.all_pieces_inline_keyboard()
    text = texts.all_pieces_text
    await message.answer(text=text, reply_markup=markup)


@dp.message(Text(text='Хочу пьесу под настроение'))
async def mood_pieces(message: Message):
    markup = await keyboards.mood_pieces_inline_keyboard()
    text = texts.mood_pieces_text
    await message.answer(text=text, reply_markup=markup)
#-----------------------------------------------------------------------------------------------------------------------
# ОБРАБОТКА ИНЛАЙН КНОПОК ВЫБОРА СОРТИРОВКИ ПЬЕС ПО АЛФАВИТУ/ДАТЕ/ЖАНРУ/СЛУЧАЙНАЯ ПЬЕСА
# по алфавиту
@dp.callback_query(CBF_Pieces.filter(F.action=='alphabet'))
async def get_alphabet_pieces(query: CallbackQuery, callback_data: CBF_Pieces):
    murkup = await keyboards.sort_inline_keyboard(sort_by='name')
    await query.message.edit_text(text=texts.alphabet_text, reply_markup=murkup)


# по дате
@dp.callback_query(CBF_Pieces.filter(F.action=='date'))
async def get_date_pieces(query: CallbackQuery, callback_data: CBF_Pieces):
    murkup = await keyboards.sort_inline_keyboard(sort_by='date')
    await query.message.edit_text(text=texts.date_text, reply_markup=murkup)


# по жанру
@dp.callback_query(CBF_Pieces.filter(F.action=='genre'))
async def get_genre_pieces(query: CallbackQuery, callback_data: CBF_Pieces):
    genre = callback_data.value
    murkup = await keyboards.sort_inline_keyboard(sort_by='genre', genre=genre)
    await query.message.edit_text(text=texts.genge_text, reply_markup=murkup)
#-----------------------------------------------------------------------------------------------------------------------


# ОБРАБОТКА ВЫБОРА КОНКРЕТНОЙ ПЬЕСЫ
@dp.callback_query(CBF_Pieces.filter(F.action=='get_piece'))
async def get_name_pieces(query: CallbackQuery, callback_data: CBF_Pieces):
    name = callback_data.name
    markup = await keyboards.info_piece_inline_keyboard(name=name)
    text = texts.info_piece_text
    await query.message.edit_text(text=text, reply_markup=markup)


# кнопка "О пьесе"
@dp.callback_query(CBF_Pieces.filter(F.action=='about_piece'))
async def about_piece(query: CallbackQuery, callback_data: CBF_Pieces):
    markup = await keyboards.back_to_mainmenu_inline_keyboard()
    name = callback_data.name
    text = await crud.get_pieces(name=name)
    await query.message.edit_text(text=text, reply_markup=markup)



#-----------------------------------------------------------------------------------------------------------------------

# ОБРАБОТКА КНОПОК "НАЗАД"
@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='main_menu'))
async def get_edit_mainmenu(query: CallbackQuery, callback_data: CBF_Pieces):
    await query.message.delete()
    await main_menu(query.message)


@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='name'))
@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='date'))
async def get_btn1_mainmenu(query: CallbackQuery, callback_data: CBF_Pieces):
    markup = await keyboards.all_pieces_inline_keyboard()
    text = texts.all_pieces_text
    await query.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='genre'))
async def get_btn2_mainmenu(query: CallbackQuery, callback_data: CBF_Pieces):
    markup = await keyboards.mood_pieces_inline_keyboard()
    text = texts.mood_pieces_text
    await query.message.edit_text(text=text, reply_markup=markup)

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())