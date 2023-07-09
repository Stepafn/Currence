import asyncio
import requests # URL processing module
from bs4 import BeautifulSoup # Module for working with HTML
import time # Module to stop the program

start = input("Enter command: ")

# Main class
class Currency:
    # Link to the desired page
    DOLLAR_RUB = 'http://www.finmarket.ru/currency/USD/'
    # Link to the desired page
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    current_converted_price = 0
    difference = 5

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def init(self):
        # Setting the exchange rate when creating an object
        self.current_converted_price = float((await self.get_currency_price()).replace(",", "."))

    # Method for getting the exchange rate
    async def get_currency_price(self):
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
        currency = float(currency.replace(",", "."))
        if currency >= self.current_converted_price + self.difference:
            print("The course has grown a lot!")
        elif currency <= self.current_converted_price - self.difference:
            print("The course has dropped a lot!")

        print("Current rate: 1 dollar = " + str(currency))
        await asyncio.sleep(30)
        await self.check_currency()

async def main():
    if start == "Currence":
        currency = Currency()
        await currency.init()
        await currency.check_currency()
    else:
        print("Error! Try again?")

if __name__ == "__main__":
    asyncio.run(main())