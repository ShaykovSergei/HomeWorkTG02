import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv
import random
import os

from gtts import gTTS
from translate import Translator

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем папку img, если она не существует
if not os.path.exists('img'):
    os.makedirs('img')

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('021426.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile('zvuk.mp3')
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile('Prompt.pdf')
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('Alan_Walker.mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_training = random.choice(training_list)
    await message.answer(f"Это ваша тренировка на сегодня {rand_training} ")

    tts = gTTS(text=rand_training, lang='ru')
    tts.save('training.ogg')
    audio = FSInputFile('training.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove('training.ogg')

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
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help \n /photo \n /video \n /audio \n /voice \n /doc \n /training')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}')

@dp.message()
async def echo(message: Message):
    if message.text.lower() == 'тест':
        await message.answer('Тест пройден!')
    else:
        translator = Translator(to_lang="en")
        translation = translator.translate(message.text)
        await message.answer(f'Перевод на английский: {translation}')

        # Отправка голосового сообщения с переводом
        tts = gTTS(text=translation, lang='en')
        tts.save('translation.ogg')
        audio = FSInputFile('translation.ogg')
        await bot.send_voice(message.chat.id, audio)
        os.remove('translation.ogg')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())