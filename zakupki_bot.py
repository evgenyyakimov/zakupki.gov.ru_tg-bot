from async_main import get_data
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os

bot = Bot(token='')
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['44 ФЗ', '223 ФЗ']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите закон', reply_markup=keyboard)


@dp.message_handler(Text(equals='44 ФЗ'))
async def fz44(message: types.Message):
    await message.answer('Парсинг....')
    chat_id = message.chat.id
    await send_data(chat_id=chat_id)


@dp.message_handler(Text(equals='223 ФЗ'))
async def fz223(message: types.Message):
    await message.answer('Парсинг этого закона временно не доступен!')
    chat_id = message.chat.id
    await send_data(chat_id=chat_id)


async def send_data(chat_id=''):
    file = await get_data()
    await bot.send_document(chat_id=chat_id, document=open(file, 'rb'))
    await os.remove(file)

if __name__ == '__main__':
    executor.start_polling(dp)
