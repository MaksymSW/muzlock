from bot_init import bot
from crud import get_all_users, change_status
import aiogram


async def send_weather():

    info = "The Wether in Kyiv is fine"
    users = get_all_users()
    for user in users:
        try:
            await bot.send_message(chat_id=user.tg_id, text=info)
        except aiogram.exceptions.TelegramForbiddenError as err:
            print(user.first_name, err)
            change_status(user.tg_id, False)
            continue
