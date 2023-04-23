from aiogram.fsm.state import StatesGroup, State

class Chouse_Piece(StatesGroup):
    fsm_sort_by = State()
    fsm_name = State()