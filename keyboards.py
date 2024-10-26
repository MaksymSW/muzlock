from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_categories_kb():
    buttons = [
        [InlineKeyboardButton(text='Bands', callback_data='cat:bands')],
        [InlineKeyboardButton(text='Musicians', callback_data='cat:musicians')],
        [InlineKeyboardButton(text='Entertainment services', callback_data='cat:services')]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def get_subcategory_kb(link: str):
    b_data = f'sub:{link}'
    if len(b_data) > 64:
        raise ValueError("subcategory-kb:Callback data is too long")
    button = [
        [InlineKeyboardButton(text='Choose', callback_data=b_data)],
        [InlineKeyboardButton(text='Go back', callback_data='back')]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=button)
    return kb

async def get_musician_kb():
    button = [
        [InlineKeyboardButton(text='Go back', callback_data='back')]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=button)
    return kb
