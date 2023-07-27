import configargparse  # imports the configargparse module, which allows you to specify program options in the configuration file.
import asyncio  # imports the asyncio module for asynchronous programming.
import requests  # imports the requests module to send HTTP requests.
from bs4 import BeautifulSoup  # imports the BeautifulSoup class from the bs4 module for parsing HTML.
import logging  # imports the logging module for logging.


class ParseIni:  # defines the ParseIni class.
    def __init__(self):  # class constructor.
        parser = configargparse.ArgParser()  # creates a command line argument parser object.
        parser.add_argument('-c', '--config', required=True, is_config_file=True, help='Path to file config.ini')
        parser.add_argument('--currency_source', default='http://www.finmarket.ru/currency/USD/',
                            help='Currency web-source')
        parser.add_argument('--sleep', default=3, type=int, help='Update delay in seconds')
        parser.add_argument('--tracking_point', default=0.5, type=float, help='Change rate point')
        parser.add_argument('--headers', default={'User-Agent': 'Mozilla/5.0'}, help='Change rate point')
        parser.add_argument('--log_config', default={"level": logging.INFO,
                                                     "format": '%(asctime)s %(levelname)s %(message)s'},
                            help='Log configs')  # adds arguments that can be passed on the command line.
        args = parser.parse_args()  # parses the passed arguments and stores them in args.
        self.currency_source = args.currency_source
        self.sleep = args.sleep
        self.tracking_point = args.tracking_point
        self.headers = args.headers
        self.log_config = args.log_config


class Currency:  # defines the Currency class.
    used_args = ParseIni()  # creates an instance of the ParseIni class and stores it in used_args.

    def __init__(self):  # class constructor.
        self.loop = asyncio.get_event_loop()
        self.previous_currency = None

    async def get_currency_price(self):  # asynchronous method for getting the exchange rate.
        full_page = await self.loop.run_in_executor(None, requests.get, self.used_args.currency_source,
                                                    headers=self.used_args.headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("div", {"class": "valvalue"})
        return convert[0].text

    async def check_currency(self):  # an asynchronous method for tracking course changes.
        logging.basicConfig(filename='log.txt', **self.used_args.log_config)
        while True:
            currency = await self.get_currency_price()
            currency = float(currency.replace(",", "."))
            if self.previous_currency is not None:
                if currency >= self.previous_currency + self.used_args.tracking_point:
                    logging.info("The course has grown a lot!")
                    print(f"The course has grown a lot! {currency}")
                elif currency <= self.previous_currency - self.used_args.tracking_point:
                    logging.info("The course has dropped a lot!")
                    print(f"The course has dropped a lot! {currency}")
            self.previous_currency = currency
            logging.info(f"Current rate: 1 dollar = {currency}")
            print(f"Current rate: 1 dollar = {currency}")
            await asyncio.sleep(self.used_args.sleep)


async def main():  # asynchronous main function.
    while True:
        try:
            start = input("Enter command: ")
            if start == "Currency":
                await Currency().check_currency()
            else:
                raise ValueError
        except ValueError:
            print("Error! Try again?")


if __name__ == "__main__":  # checks if the script is run directly and not imported as a module.
    asyncio.run(main())  # starts an asynchronous loop with a call to the main() function.
