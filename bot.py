import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import configparser

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read("config.txt")
bot_token = config.get('bot', 'token')

bot = Bot(token=bot_token)
dp = Dispatcher()


@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    logging.info('Received /start command')
    await message.answer('Hi! I am a bot that can add 1 + 1')


@dp.message(F.text == '1+1')
async def cmd_answer(message: Message):
    await message.answer('Answer 3')


@dp.message()
async def echo(message: Message):
    await message.answer('Unknown command. I can only add 1 + 1')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

