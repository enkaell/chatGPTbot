import logging
import random
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the bot and dispatcher
bot = Bot(token='5850584012:AAHbiwNrmZFRbkqliL7BcWlgDDYBcWNm5Zc')
dp = Dispatcher(bot)


# Command handlers
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет, напиши /help чтобы увидеть мои возможности")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Привет, вот что я могу:\n"
                         "/dice - бросить кубик\n"
                         "/coinflip - подкинуть монетку\n"
                         "/quote - получить цитату на английском\n"
                         "/cat - получить котенка")


@dp.message_handler(commands=['dice'])
async def dice_command(message: types.Message):
    await message.reply(f"Тебе выпало {random.randint(1, 6)}.")


@dp.message_handler(commands=['coinflip'])
async def coinflip_command(message: types.Message):
    result = random.choice(['heads', 'tails'])
    await message.reply(f"Монетка упала {result}.")


@dp.message_handler(commands=['quote'])
async def quote_command(message: types.Message):
    # Get a random quote from an API
    response = requests.get('https://api.quotable.io/random')
    if response.status_code == 200:
        data = response.json()
        await message.reply(data['content'])
    else:
        await message.reply("Sorry, something went wrong.")


@dp.message_handler(commands=['cat'])
async def cat_command(message: types.Message):
    # Get a random cat picture from an API
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    if response.status_code == 200:
        data = response.json()
        await bot.send_photo(message.chat.id, data[0]['url'])
    else:
        await message.reply("Sorry, something went wrong.")


# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
