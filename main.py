import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

# @dp.message(Command('photo', prefix='&'))
@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://img.freepik.com/premium-photo/picture-supercar-speeding-wallpaper_670382-69999.jpg?semt=ais_hybrid ', 'https://i.pinimg.com/originals/60/24/40/6024403726666384d2599d5990b72247.jpg?nii=t ', 'https://img.freepik.com/free-photo/futuristic-supercar_23-2151955591.jpg?semt=ais_hybrid&w=740&q=80 ']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер тачка!')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого какая фотка!', 'Непонятно, что это такое?', 'Не отправляйте мне такое больше фото!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')


@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help \n /photo')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}')
    # await message.answer(f'Привет, {message.from_user.full_name}')
    # await message.answer('Привет! Я бот.')

# @dp.message()
# async def start(message: Message):
#     await message.answer('Я не понимаю это сообщение.')

# @dp.message()
# async def echo(message: Message):
#     await message.send_copy(chat_id=message.chat.id)

@dp.message()
async def echo(message: Message):
    if message.text.lower() == 'тест':
        await message.answer('Тест пройден!')


async def main():
    await  dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())