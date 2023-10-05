import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

bot = Bot(token='6500524410:AAElwMSMO8zD72UHtqRh9OBPJnh4LCifkc8')
dp = Dispatcher()


@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer('Hi! I am a bot that can add 1 + 1')


@dp.message(F.text == '1+1')
async def cmd_1(message: Message):
    await message.answer('Answer 3')


@dp.message()
async def echo(message: Message):
    await message.answer('Unknown command. I can only add 1 + 1')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
