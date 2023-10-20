import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from parsers import ParseIni
from logger import get_logger

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
    cfg = ParseIni()
    logger = get_logger(cfg.log_config.get('level'),
                        cfg.log_config.get('format'),
                        cfg.log_config.get('filename'))
    token = cfg.token
    bot = Bot(token)

    asyncio.run(main())
