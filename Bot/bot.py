# файлы проекта
import pathlib

import crud
import keyboards
import texts

from CBFactories import CBF_Pieces

# отдельные импорты
import logging
import asyncio
import os
from pathlib import Path
from magic_filter import F
from dotenv import load_dotenv

# импорты aiogram
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile





load_dotenv()

token = os.getenv('BOTTOKEN')
storage = MemoryStorage()

bot = Bot(token)
dp = Dispatcher(storage=storage)

# запись логов в файл
logging.basicConfig(level=logging.INFO,
                    filename='bot_log.txt',
                    filemode='w',
                    format= '%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z')


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

    # получаем полный путь к гиф изображению
    current_path = pathlib.Path(__file__).resolve().parents[1]
    gif_path = Path(current_path, 'media', 'images', 'Приветствие.mp4')

    # получаем гиф изображение
    gif = FSInputFile(gif_path)

    await message.answer_animation(caption=text, animation=gif, reply_markup=markup)

@dp.message(Command(commands=['menu']))
@dp.message(Text(text='Главное меню'))
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
    markup = await keyboards.all_pieces_keyboard()
    text = texts.all_pieces_text
    await message.answer(text=text, reply_markup=markup)


@dp.message(Text(text='Хочу пьесу под настроение'))
async def mood_pieces(message: Message):
    markup = await keyboards.mood_pieces_keyboard()
    text = texts.mood_pieces_text
    await message.answer(text=text, reply_markup=markup)


@dp.message(Text(text='Авторы'))
async def about_authors(message: Message):
    # получаем полный путь к изображению
    current_path = pathlib.Path(__file__).resolve().parents[1]
    photo_path = Path(current_path, 'media', 'images', 'authors.jpg')

    # получаем изображение
    photo = FSInputFile(photo_path)

    text = texts.about_authors_text
    await message.answer_photo(caption=text, photo=photo)
#-----------------------------------------------------------------------------------------------------------------------

#ОБРАБОТКА КНОПОК МЕНЮ (про все пьесы)
# в состояние при нажатии на каждую кнопку записываем sort_by и genre для последующей реализации
# инлайн кнопок с номерами страниц
# в последующем эти действия повторяются для всех кнопок вывода списка пьес
@dp.message(Text(text='По алфавиту'))
async def sort_alphabet_pieces(message: Message, state: FSMContext):
    await state.update_data(sort_by='name',
                            genre=None,
                            text=texts.alphabet_text)

    list_dicts_pieces = await crud.get_pieces_sort(sort_by='name')
    markup = await keyboards.pieces_inline_keyboard(list_dicts_pieces)

    await message.answer(text=texts.alphabet_text, reply_markup=markup)

@dp.message(Text(text='По дате'))
async def sort_date_pieces(message: Message, state: FSMContext):
    await state.update_data(sort_by='date',
                            genre=None,
                            text=texts.date_text)

    list_dicts_pieces = await crud.get_pieces_sort(sort_by='date')
    markup = await keyboards.pieces_inline_keyboard(list_dicts_pieces)

    await message.answer(text=texts.date_text, reply_markup=markup)


@dp.message(Text(text='Случайная пьеса'))
async def random_piece(message: Message, state: FSMContext):
    id_piece = await crud.get_random_piece()

    # получили данные о пьесе в виде словаря
    dict_info_piece = await crud.piece_info_by_id(id_piece)

    # пробуем получить изображение из БД
    # Если оно есть, то выводим изображение, если нет, то выводим просто текст из БД
    try:
        image = await crud.piece_img_by_id(id_piece)
        await message.answer_photo(photo=image)
    except:
        pass

    # записали данные в состояние
    await state.update_data(dict_info_piece=dict_info_piece)

    # разметка клавиатуры и текст
    markup = await keyboards.info_piece_inline_keyboard()
    text = dict_info_piece['description_piece']

    await message.answer(text=text, reply_markup=markup)


#-----------------------------------------------------------------------------------------------------------------------

#ОБРАБОТКА КНОПОК МЕНЮ (пьесы под настроение)
@dp.message(Text(text='Комедии'))
async def comedy_piece(message: Message, state: FSMContext):
    await state.update_data(sort_by='genre',
                            genre='Комедия',
                            text=texts.comedi_text)

    list_dicts_pieces = await crud.get_pieces_sort(sort_by='genre', genre='Комедия')
    markup = await keyboards.pieces_inline_keyboard(list_dicts_pieces)

    await message.answer(text=texts.comedi_text, reply_markup=markup)


@dp.message(Text(text='Драмы'))
async def dramas_piece(message: Message, state: FSMContext):
    await state.update_data(sort_by='genre',
                            genre='Драма',
                            text=texts.drama_text)

    list_dicts_pieces = await crud.get_pieces_sort(sort_by='genre', genre='Драма')
    markup = await keyboards.pieces_inline_keyboard(list_dicts_pieces)

    await message.answer(text=texts.drama_text, reply_markup=markup)


@dp.message(Text(text='Малоизвестные пьесы'))
async def non_popular_piece(message: Message, state: FSMContext):
    await state.update_data(sort_by='non_popular',
                            genre=None,
                            text=texts.non_popular_text)

    list_dicts_pieces = await crud.get_pieces_sort(sort_by='non_popular')
    markup = await keyboards.pieces_inline_keyboard(list_dicts_pieces)

    await message.answer(text=texts.non_popular_text, reply_markup=markup)
#-----------------------------------------------------------------------------------------------------------------------
# ОБРАБОТКА ИНЛАЙН КНОПОК С НОМЕРАМИ СТРАНИЦ
@dp.callback_query(CBF_Pieces.filter(F.action=='page'))
async def page_selection(query: CallbackQuery, callback_data: CBF_Pieces, state: FSMContext):
    '''
    Функция вызывается при нажатии на кнопку с номером страницы
    data это данные записанные в FSM состоянии
    Мы получаем оттуда sort_by и genre чтобы вызвать функцию из crud
    А дальше происходит тоже самое что и при нажатии на одну из кнопок меню, за исключением того что
    в keyboard передается номер страницы с пьесами которые нужно вывести и сообщение редактируется
    так как на данном моменте у пользователя висит в чате инлайн клавиатура 
    '''
    data = await state.get_data()

    list_dicts_pieces = await crud.get_pieces_sort(sort_by=data['sort_by'],
                                              genre=data['genre'])
    markup = await keyboards.pieces_inline_keyboard(list_dicts_pieces,
                                                    page=callback_data.page_number)

    await query.message.edit_text(text=data['text'], reply_markup=markup)
#-----------------------------------------------------------------------------------------------------------------------
# ОБРАБОТКА ИНЛАЙН КНОПОК С ПЬЕСАМИ
# при нажатии на пьесу
@dp.callback_query(CBF_Pieces.filter(F.action=='get_piece'))
async def get_piece_info(query: CallbackQuery, callback_data: CBF_Pieces, state: FSMContext):
    '''

    '''
    # получили данные о пьесе в виде словаря
    dict_info_piece = await crud.piece_info_by_id(callback_data.id_piece)

    # записали данные в состояние
    await state.update_data(dict_info_piece=dict_info_piece)

    # разметка клавиатуры и текст
    markup = await keyboards.info_piece_inline_keyboard()
    text = dict_info_piece['description_piece']

    # пробуем получить изображение из БД
    # Если оно есть, то выводим изображение, если нет, то выводим просто текст из БД
    try:
        image = await crud.piece_img_by_id(callback_data.id_piece)
        await query.message.answer_photo(photo=image)
    except: pass

    await query.message.answer(text=text, reply_markup=markup)


# при нажатии на "Сюжет"
@dp.callback_query(CBF_Pieces.filter(F.action=='detail'))
async def get_detail_piece_info(query: CallbackQuery, callback_data: CBF_Pieces, state: FSMContext):
    data = await state.get_data()                           # данные из состояния
    dict_info_piece = data['dict_info_piece']               # словарь с информацией о пьесе
    text = dict_info_piece['description_piece_detailed']    # текс "Подробнее"
    id_piece = dict_info_piece['id']                        # id пьесы

    # в клавиатуру передаем id пьесы для реализации кнопки "Назад"
    markup = await keyboards.detailed_info_piece_inline_keyboard(id_piece)

    await query.message.answer(text=text, reply_markup=markup)


# при нажатии на "О постановке"
@dp.callback_query(CBF_Pieces.filter(F.action=='info_play'))
async def about_play(query: CallbackQuery, callback_data: CBF_Pieces, state: FSMContext):
    data = await state.get_data()               # данные из состояния
    dict_info_piece = data['dict_info_piece']   # словарь с информацией о пьесе
    text = dict_info_piece['description_play']  # текс "О постановке"
    id_piece = dict_info_piece['id']            # id пьесы

    # в клавиатуру передаем id пьесы для реализации кнопки "Назад"
    markup = await keyboards.about_play_piece_inline_keyboard(id_piece)

    await query.message.answer(text=text, reply_markup=markup)


# при нажатии на "Сходить на постановку"
@dp.callback_query(CBF_Pieces.filter(F.action=='go_play'))
async def links_piece(query: CallbackQuery, callback_data: CBF_Pieces, state: FSMContext):
    data = await state.get_data()  # данные из состояния
    dict_info_piece = data['dict_info_piece']  # словарь с информацией о пьесе
    link_play = dict_info_piece['link_play']
    link_video = dict_info_piece['link_video']
    text = f'Если хотите сходить на постановку, то перейдите по этой ссылке\n' \
           f'⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️\n\n\n' \
           f'{link_play}' \
           f'\n\n\n' \
           f'Если вам лень куда-то ходить, то можно посмотреть пьесу в записи\n' \
           f'⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️\n\n\n' \
           f'{link_video}'


    id_piece = dict_info_piece['id']  # id пьесы

    # в клавиатуру передаем id пьесы для реализации кнопки "Назад"
    markup = await keyboards.go_play_piece_inline_keyboard(id_piece)

    await query.message.answer(text=text, reply_markup=markup)

#-----------------------------------------------------------------------------------------------------------------------
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())