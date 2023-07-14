import configargparse  # To run a Python script using additional arguments on the command line and passing variables
import asyncio  # allows you to do asynchronous programming
import requests  # URL processing module
from bs4 import BeautifulSoup  # Module for working with HTML
import logging  # allows you to write logs to a file:


class ParseIni:

    def __init__(self):
        parser = configargparse.ArgParser()
        parser.add_argument('-c', '--config', required=True, is_config_file=True, help='Path to file config.ini')
        parser.add_argument('--dollar_rub', help='ruble exchange rate')
        parser.add_argument('--sleep', help='Пауза')
        parser.add_argument('--tracking_point', help='change rate point')
        args = parser.parse_args()
        self.dollar_rub = args.dollar_rub
        self.sleep = args.sleep
        self.tracking_point = args.tracking_point


# Main class
class Currency:
    """Link to the desired page"""
    parse = ParseIni()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def get_currency_price(self):
        """Method for getting the exchange rate"""
        # Parse the entire page
        full_page = await self.loop.run_in_executor(None, requests.get, self.parse.dollar_rub,
                                                    {'headers': self.headers})
        # Parsing through BeautifulSoup
        soup = BeautifulSoup(full_page.content, 'html.parser')

        # Get the value we need and return it
        convert = soup.findAll("div", {"class": "valvalue"})
        return convert[0].text

    async def check_currency(self):
        """Check currency change"""
        logging.basicConfig(filename='log.txt', level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')
        while True:
            currency = await self.get_currency_price()
            currency = float(currency.replace(",", "."))
            if currency >= currency + float(self.parse.tracking_point):
                logging.info("The course has grown a lot!")
            elif currency <= currency - float(self.parse.tracking_point):
                logging.info("The course has dropped a lot!")
            logging.info(f"Current rate: 1 dollar = {str(currency)}")
            await asyncio.sleep(int(self.parse.sleep))


async def main():
    while True:
        try:
            start: str = input("Enter command: ")
            if start == "Currency":
                await Currency().check_currency()
            raise ValueError
        except ValueError:
            print("Error! Try again?")


if __name__ == "__main__":
    asyncio.run(main())
