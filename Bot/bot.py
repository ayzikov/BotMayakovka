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
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage





load_dotenv()

token = os.getenv('BOTTOKEN')
storage = MemoryStorage()

bot = Bot(token)
dp = Dispatcher(storage=storage)
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
async def get_alphabet_pieces(query: CallbackQuery, state: FSMContext):
    markup = await keyboards.sort_inline_keyboard(sort_by='name')
    await query.message.edit_text(text=texts.alphabet_text, reply_markup=markup)

    await state.update_data(message_id=query.message.message_id,
                            markup=markup,
                            text=texts.alphabet_text)


# по дате
@dp.callback_query(CBF_Pieces.filter(F.action=='date'))
async def get_date_pieces(query: CallbackQuery, state: FSMContext):
    markup = await keyboards.sort_inline_keyboard(sort_by='date')
    await query.message.edit_text(text=texts.date_text, reply_markup=markup)
    await state.update_data(message_id=query.message.message_id,
                            markup=markup,
                            text=texts.date_text)


# по жанру
@dp.callback_query(CBF_Pieces.filter(F.action=='genre'))
async def get_genre_pieces(query: CallbackQuery, callback_data: CBF_Pieces, state: FSMContext):
    genre = callback_data.value
    markup = await keyboards.sort_inline_keyboard(sort_by='genre', genre=genre)
    await query.message.edit_text(text=texts.genge_text, reply_markup=markup)
    await state.update_data(message_id=query.message.message_id,
                            markup=markup,
                            text=texts.genge_text)


# малоизвестные
@dp.callback_query(CBF_Pieces.filter(F.action=='non_popular'))
async def get_non_popular_pieces(query: CallbackQuery, state: FSMContext):
    markup = await keyboards.sort_inline_keyboard(sort_by='non_popular')
    await query.message.edit_text(text=texts.non_popular_text, reply_markup=markup)
    await state.update_data(message_id=query.message.message_id,
                            markup=markup,
                            text=texts.non_popular_text)


# случайная пьеса
@dp.callback_query(CBF_Pieces.filter(F.action=='random'))
async def get_random_piece(query: CallbackQuery, state: FSMContext):
    response = await crud.get_pieces(random=True)
    name = response['name']
    id = response['id']

    markup = await keyboards.info_piece_inline_keyboard(id=id, random=True)
    await query.message.edit_text(text=name, reply_markup=markup)

    # запись всех данных о выбранной пьесе
    data = await crud.get_piece_description_by_id(id)

    try:
        img = await crud.get_piece_img_by_id(id)
        await state.update_data(img=img)
    except: pass

    await state.update_data(description_piece=data['description_piece'],
                            description_piece_detailed=data['description_piece_detailed'],
                            description_play=data['description_play'])

    # запись данных необходимых для реализации кнопки "Назад"
    await state.update_data(message_id_piece=query.message.message_id,
                            chat_id=query.message.chat.id,
                            markup_piece=markup,
                            text_piece=name)
#-----------------------------------------------------------------------------------------------------------------------


# ОБРАБОТКА ВЫБОРА КОНКРЕТНОЙ ПЬЕСЫ
@dp.callback_query(CBF_Pieces.filter(F.action=='get_piece'))
async def get_name_pieces(query: CallbackQuery, callback_data: CBF_Pieces, state: FSMContext):
    id = callback_data.id
    name = await crud.get_piece_name_by_id(id=id)

    markup = await keyboards.info_piece_inline_keyboard(id=id)

    try:
        await query.message.edit_text(text=name, reply_markup=markup)
    except:
        await query.message.answer(text=name, reply_markup=markup)

    # запись всех данных о выбранной пьесе
    data = await crud.get_piece_description_by_id(id)

    try:
        img = await crud.get_piece_img_by_id(id)
        await state.update_data(img=img)
    except: pass

    await state.update_data(description_piece=data['description_piece'],
                            description_piece_detailed=data['description_piece_detailed'],
                            description_play=data['description_play'])

    # запись данных необходимых для реализации кнопки "Назад"
    await state.update_data(message_id_piece=query.message.message_id,
                            chat_id=query.message.chat.id,
                            markup_piece=markup,
                            text_piece=name,
                            query=query,
                            callback_data=callback_data)


# кнопка "О пьесе"
@dp.callback_query(CBF_Pieces.filter(F.action=='about_piece'))
async def about_piece(query: CallbackQuery, state: FSMContext):
    markup = await keyboards.about_piece_inline_keyboard()

    data = await state.get_data()
    chat_id = data['chat_id']
    text = data['description_piece']

    try:
        img = data['img']

        await query.message.delete()
        await query.message.answer_photo(photo=img, caption=text, reply_markup=markup)

    except:
        await query.message.edit_text(text=text, reply_markup=markup)



# кнопка "Подробнее"
@dp.callback_query(CBF_Pieces.filter(F.action=='more'))
async def more_about_piece(query: CallbackQuery, state: FSMContext):
    markup = await keyboards.more_about_piece_inline_keyboard()

    data = await state.get_data()
    text = data['description_piece_detailed']

    try:
        await query.message.edit_text(text=text, reply_markup=markup)
    except:
        await query.message.delete()
        await query.message.answer(text=text, reply_markup=markup)


# кнопка "О постановке"
@dp.callback_query(CBF_Pieces.filter(F.action=='about_play'))
async def about_play(query: CallbackQuery, state: FSMContext):
    markup = await keyboards.about_play_inline_keyboard()

    data = await state.get_data()
    text = data['description_play']

    await query.message.edit_text(text=text, reply_markup=markup)

# кнопка "Сходить на постановку"
@dp.callback_query(CBF_Pieces.filter(F.action=='go_play'))
async def go_to_the_play(query: CallbackQuery):
    markup = await keyboards.go_to_the_play_inline_keyboard()
    text = 'Ссылка на постановку'
    await query.message.edit_text(text=text, reply_markup=markup)





#-----------------------------------------------------------------------------------------------------------------------

# ОБРАБОТКА КНОПОК "НАЗАД"
@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='main_menu'))
async def get_edit_mainmenu(query: CallbackQuery, callback_data: CBF_Pieces):
    await query.message.delete()
    await main_menu(query.message)


@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='name'))
@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='date'))
async def get_btn1_mainmenu(query: CallbackQuery):
    markup = await keyboards.all_pieces_inline_keyboard()
    text = texts.all_pieces_text
    await query.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='genre'))
@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='non_popular'))
async def get_btn2_mainmenu(query: CallbackQuery, callback_data: CBF_Pieces):
    markup = await keyboards.mood_pieces_inline_keyboard()
    text = texts.mood_pieces_text
    await query.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='state'))
async def get_state_back(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data['message_id']
    markup = data['markup']
    text = data['text']

    await bot.edit_message_text(text=text,
                                chat_id=query.message.chat.id,
                                message_id=message_id,
                                reply_markup=markup)


@dp.callback_query(CBF_Pieces.filter(F.action=='back' and F.value=='state_piece'))
async def get_state_back(query: CallbackQuery, callback_data: CBF_Pieces, state: FSMContext):
    data = await state.get_data()
    message_id = data['message_id_piece']
    markup = data['markup_piece']
    text = data['text_piece']


    try:
        await bot.edit_message_text(text=text,
                                    chat_id=query.message.chat.id,
                                    message_id=message_id,
                                    reply_markup=markup)
    except:
        await query.message.delete()
        query = data['query']
        callback_data = data['callback_data']
        await get_name_pieces(query, callback_data, state)



async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())