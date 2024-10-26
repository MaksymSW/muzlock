from crud import create_user
from info_handler import send_weather
import asyncio


if __name__ == "__main__":
    # create_user('Bob', 'Tompson', 25478, 'UA')
    asyncio.run(send_weather())
    