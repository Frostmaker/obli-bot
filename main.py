import logging
import os
from os import getenv, environ
from sys import exit
from aiogram import Bot, Dispatcher, executor, types

PORT = int(environ.get('PORT', 3001))
TOKEN = getenv('TOKEN')
if not TOKEN:
    exit('Error: no token provided')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Список облигаций')
    await message.answer("Hello! I'm Obli!\n"
                         "I'll help you with bonds.\n\n"
                         "Available commands:\n"
                         "/\n"
                         "/\n"
                         "/\n", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def send_help(message):
    '''
    This handler will be called when user sends `/help` command
    :param message:
    :return:
    '''
    await message.answer("Help Here")


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def test(message: types.Message):
    print('Start downloading....')
    await message.document.download(destination_dir='temp/')
    print('File downloaded.')
    await message.answer('Document saved.')


@dp.message_handler(commands="dinner")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text="С пюрешкой"), "Без пюрешки"]
    keyboard.add(*buttons)
    button_2 = "🍵"
    keyboard.add(button_2)
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer('Я не знаю такой команды.')


if __name__ == '__main__':
    executor.start_polling(dp)
    executor.start_webhook(dispatcher=dp, )