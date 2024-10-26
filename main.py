""" main file"""
import asyncio
import logging
import sys
from aiogram import html, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot_init import dp, bot  # , config
from crud import create_user
from keyboards import get_categories_kb, get_subcategory_kb, get_musician_kb
from muz_parser import get_subcategories, get_musicians


BASE_URL = 'https://www.lastminutemusicians.com'
YOUTUBE_URL = 'https://youtu.be/'


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command.

    Most event objects have aliases for API methods that can be called in events' context
    For example if you want to answer to incoming message you can use `message.answer(...)` alias
    and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    method automatically or call API method directly via
    Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    """

    keyboard = await get_categories_kb()
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=keyboard
    )
    create_user(
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        tg_id=message.from_user.id,
        lang=message.from_user.language_code
    )


@dp.callback_query(F.data.startswith('back'))
async def go_back(callback: types.CallbackQuery):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Returning to categories...",
        reply_markup=await get_categories_kb()
    )


async def separator(callback: types.CallbackQuery):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Sending data...\n",
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith('cat'))
async def category_handler(callback: types.CallbackQuery):
    """_summary_

    Args:
        callback (types.CallbackQuery): _description_
    """
    data = callback.data
    command = data.split(':')[1]
    await separator(callback)
    match command:
        case 'bands':
            subcats = get_subcategories('/bands.html')
        case 'musicians':
            subcats = get_subcategories('/musicians.html')
        case 'services':
            subcats = get_subcategories('/entertainment-services.html')
    for subs in subcats:
        await bot.send_photo(
            chat_id=callback.from_user.id,
            photo=subs.get('image_bg'),
            caption=f"{subs.get('title')}\n{subs.get('members')}",
            reply_markup=await get_subcategory_kb(subs.get('link'))
        )


@dp.callback_query(F.data.startswith('sub'))
async def subcategory_handler(callback: types.CallbackQuery):
    """_summary_

    Args:
        callback (types.CallbackQuery): _description_
    """
    data = callback.data
    command = data.split(':')[1]
    await separator(callback)
    musicians = get_musicians(command)
    for muz in musicians:
        match muz.get('media_type'):
            case 'image':
                await bot.send_photo(
                    chat_id=callback.from_user.id,
                    photo=BASE_URL + muz.get('media_link'),
                    caption=f"{muz.get('title')}\n\n"
                        f"{muz.get('description')}\n"
                        f"Located at: {muz.get('location')}\n"
                        f"Average price: {muz.get('price')}\n\n"
                        f"Link to site: {muz.get('link')}",
                    reply_markup=await get_musician_kb()
                )
            case 'video':
                link = YOUTUBE_URL + muz.get('media_link')
                print(link)
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text=f"{muz.get('title')}\n\n"
                        f"{muz.get('description')}\n"
                        f"Located at: {muz.get('location')}\n"
                        f"Average price: {muz.get('price')}\n\n"
                        f"Link to site: {muz.get('link')}\n\n"
                        f"🎥 [Watch Video]({link})",
                    parse_mode="Markdown",
                    reply_markup=await get_musician_kb()
                )
            case 'audio':
                await bot.send_audio(
                    chat_id=callback.from_user.id,
                    audio=BASE_URL + muz.get('media_link'),
                    caption=f"{muz.get('title')}\n\n"
                        f"{muz.get('description')}\n"
                        f"Located at: {muz.get('location')}\n"
                        f"Average price: {muz.get('price')}\n\n"
                        f"Link to site: {muz.get('link')}",
                    reply_markup=await get_musician_kb()
                )


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    """Initialize Bot instance with default bot properties which will be passed
    to all API calls. And the run events dispatching"""
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    asyncio.run(main())
