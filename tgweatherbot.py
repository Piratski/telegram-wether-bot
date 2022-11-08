from email import message
from imaplib import Commands
import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor



bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Write were you wan`t to know wether")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_smile = {
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Rain \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B",
    }


    
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        current_temp = data["main"]["temp"]

        weather_desc = data["weather"][0]["main"]
        if weather_desc in code_smile:
            wd = code_smile[weather_desc]
        else:
            wd = "IDK what`s going on outside your window"


        current_humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        len_of_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Wether in city: {city}\nTemp: {current_temp}C° {wd}\n"
              f"Humidity: {current_humidity}%\nPressure: {pressure} mm\nWind: {wind} m/s\n" 
              f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nLenght of day: {len_of_day}"
              )

    
    except:
        await message.reply("\U00002620 Это точно город? \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)