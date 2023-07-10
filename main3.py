# давай осмысленные названия программе. main3.py - лучше main.py
# удали ненужные файлы (ppy)

import asyncio # где тут коммент? если пишешь комменты для остальных строк - пиши и тут
import requests # URL processing module
from bs4 import BeautifulSoup # Module for working with HTML

# где файл requirements.txt?

import time # Module to stop the program
# ты не используешь этот модуль
# настрой себе code inspector. не присылай мне код, в котором есть исправимые замечания

# почему этот тут, а не в main?
start = input("Enter command: ")

# Main class
class Currency:
    # Link to the desired page
    # вынеси во внешний конфигурационный файл. используй configargparse
    DOLLAR_RUB = 'http://www.finmarket.ru/currency/USD/'
    # зачем этот коммент? ниже.
    # Link to the desired page
    # вынеси в конфиг файл
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    current_converted_price = 0
    # из названия переменной непонятно зачем она
    difference = 5

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def init(self):
        # Setting the exchange rate when creating an object
        # сделай так, чтобы все преобразования формата были внутри get_currency_price
        self.current_converted_price = float((await self.get_currency_price()).replace(",", "."))

    # Method for getting the exchange rate
    async def get_currency_price(self):
        # где docstrings?
        # где написано какой формат данных вовзращает функция?
        # https://towardsdatascience.com/13-tips-for-using-pytest-5341e3366d2d
        # Parse the entire page
        full_page = await self.loop.run_in_executor(None, requests.get, self.DOLLAR_RUB, {'headers': self.headers})

        # Parsing through BeautifulSoup
        soup = BeautifulSoup(full_page.content, 'html.parser')

        # Get the value we need and return it
        convert = soup.findAll("div", {"class": "valvalue"})
        return convert[0].text

    # Check currency change
    async def check_currency(self):
        currency = await self.get_currency_price()
        # дублирующийся код
        currency = float(currency.replace(",", "."))

        # подумай - при каком currency у тебя выполнится второе условие - та часть, где знак равно.
        # про знак меньше - я понимаю. я про равно спрашиваю, про второе.
        if currency >= self.current_converted_price + self.difference:
            # не используй принт - начинай использовать logging
            print("The course has grown a lot!")
        elif currency <= self.current_converted_price - self.difference:
            print("The course has dropped a lot!")

        # почитай как можно выводить строки https://www.geeksforgeeks.org/python-output-formatting/
        # используй logging
        print("Current rate: 1 dollar = " + str(currency))
        # никаких hardcoded values - вынеси в конфиг, пусть 30 будет умолчанием
        await asyncio.sleep(30)
        # каждый вызов функции создает запись в стеке вызовов. каждый возврат - убирает запись
        # в твоем случае - ты устраиваешь рекурсию там, где не нужно. перепиши на цикле while True:
        await self.check_currency()

async def main():
    # не понял как это работает
    # слово валюта - с ошибкой написано
    if start == "Currence":

        # зачем вообще создавать тут объект? в чем преимущества?
        currency = Currency()
        # зачем отдельный init?
        await currency.init()
        await currency.check_currency()
    else:
        # где ты предлагаешь ему сделать try again?
        print("Error! Try again?")

if __name__ == "__main__":
    asyncio.run(main())