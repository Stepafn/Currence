import asyncio
import os
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from logger import get_logger
from dotenv import load_dotenv

load_dotenv("config.env")

dp = Dispatcher()


@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    logger.info('Received /start command')
    await message.answer('Hi! I am a bot that can add 1 + 1')


@dp.message(F.text == '1+1')
async def cmd_answer(message: Message):
    logger.info('Received "1+1" command')
    await message.answer('Answer 3')


@dp.message()
async def echo(message: Message):
    logger.info('Received an unknown command')
    await message.answer('Unknown command. I can only add 1 + 1')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    log_cfg = json.loads(os.getenv('log_config'))
    logger = get_logger(log_cfg.get('level'),
                        log_cfg.get('format'),
                        log_cfg.get('filename'))
    bot = Bot(os.getenv('token'))
    asyncio.run(main())
    
