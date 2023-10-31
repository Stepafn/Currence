import asyncio
import configargparse
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from logger import get_logger

dp = Dispatcher()

parser = configargparse.ArgParser()
parser.add_argument('--log-file', env_var='LOG_FILE', required=True, help='Log file')
parser.add_argument('--log-level', env_var='LOG_LEVEL', default='INFO', help='Log level')
parser.add_argument('--bot-token', env_var='BOT_TOKEN', required=True, help='bot token')
parser.add_argument('--log-format', env_var='LOG_FORMAT', default='%(asctime)s %(levelname)s %(message)s')

config = parser.parse_args()


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
    logger = get_logger(config.log_level,
                        config.log_format,
                        config.log_file)

    bot = Bot(config.bot_token)
    asyncio.run(main())
