from aiogram.filters.callback_data import CallbackData
from typing import Optional
class CBF_Pieces(CallbackData, prefix='pieces'):
    action: str
    id_piece: Optional[int]
    page_number: Optional[int]

