import logging
import os
from sys import exit
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    exit('Error: no token provided')

WEBHOOK_HOST = 'https://obli-bot.herokuapp.com/'
WEBHOOK_PATH = f'{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
HOST = '0.0.0.0'
PORT = int(os.getenv('PORT'))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

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
                         "/help - for additional information\n"
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


@dp.message_handler(content_types=['photo'])
async def echo_photo(message: types.Message):
    await message.answer_photo(message.photo[-1].file_id)
    await message.answer('test message')


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


@dp.message_handler(lambda message: message.text=='С пюрешкой')
async def with_puree(message: types.Message):
    await message.answer("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer('Я не знаю такой команды.')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.warning('Bot started....')


async def on_shutdown(dp):
    logging.warning('Bot shutting down....')
    # await bot.delete_webhook()


if __name__ == '__main__':
    # executor.start_polling(dp)
    executor.start_webhook(dispatcher=dp,
                           webhook_path=WEBHOOK_PATH,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           port=PORT)