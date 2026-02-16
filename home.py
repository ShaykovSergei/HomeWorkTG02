import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
import os
import aiohttp
import random

load_dotenv()
TOKEN = os.getenv('TOKEN')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

if not TOKEN:
    raise ValueError("Токен не найден в .env файле")
if not OPENWEATHER_API_KEY:
    raise ValueError("OpenWeather API ключ не найден в .env файле")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('photo'))
async def photo(message: Message):
    photos = [
        'https://img.freepik.com/premium-photo/picture-supercar-speeding-wallpaper_670382-69999.jpg?semt=ais_hybrid',
        'https://i.pinimg.com/originals/60/24/40/6024403726666384d2599d5990b72247.jpg?nii=t',
        'https://img.freepik.com/free-photo/futuristic-supercar_23-2151955591.jpg?semt=ais_hybrid&w=740&q=80'
    ]
    rand_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption='Это супер тачка!')


@dp.message(F.photo)
async def react_photo(message: Message):
    answers = ['Ого какая фотка!', 'Непонятно, что это такое?', 'Не отправляйте мне такое больше фото!']
    rand_answ = random.choice(answers)
    await message.answer(rand_answ)


@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help \n /photo \n /pogoda <город>')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот.')


@dp.message(Command('pogoda'))
async def pogoda(message: Message):
    args = message.text.split(' ', 1)
    city = args[1].strip() if len(args) > 1 else 'Москва'

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    weather = data['weather'][0]['description'].capitalize()
                    temp = data['main']['temp']
                    humidity = data['main']['humidity']
                    city_name = data['name']
                    await message.answer(
                        f"🏙 Город: {city_name}\n"
                        f"🌡 Температура: {temp}°C\n"
                        f"☁ Погода: {weather}\n"
                        f"💧 Влажность: {humidity}%"
                    )
                elif response.status == 404:
                    await message.answer(f"❌ Город '{city}' не найден. Проверьте название.")
                else:
                    await message.answer(f"⚠️ Ошибка от сервера погоды: статус {response.status}")
    except aiohttp.ClientConnectorError:
        await message.answer("🌐 Не удалось подключиться к сервису погоды. Проверьте интернет-соединение.")
    except asyncio.TimeoutError:
        await message.answer("⏰ Время ожидания ответа от сервера истекло. Попробуйте позже.")
    except Exception as e:
        await message.answer(f"🔧 Произошла ошибка: {str(e)}")


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())