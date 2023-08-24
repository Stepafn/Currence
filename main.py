import configargparse
import asyncio
import requests
from bs4 import BeautifulSoup
import logging
import json


class ParseIni:
    def __init__(self):
        parser = configargparse.ArgParser()
        parser.add_argument('-c, --config', required=True, is_config_file=True,
                            help='Path to file config.ini')
        parser.add_argument('--currency_source',
                            default='http://www.finmarket.ru/currency/USD/',
                            help='Currency web-source')
        parser.add_argument('--sleep', default=3,
                            help='Update delay in seconds')
        parser.add_argument('--tracking_point', default=0.5,
                            help='Change rate point')
        parser.add_argument('--headers', default={'User-Agent': 'Mozilla/5.0'},
                            help='Change rate point')
        parser.add_argument('--log_config',
                            default={"level": logging.INFO,
                                     "format": "%(asctime)s %(levelname)s %(message)s"},
                            help='Log configs')
        args = parser.parse_args()
        self.currency_source = args.currency_source
        self.sleep = args.sleep
        self.tracking_point = args.tracking_point
        self.headers = args.headers
        self.log_config = args.log_config


class Currency:
    used_args = ParseIni()

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def get_currency_price(self):
        full_page = await self.loop.run_in_executor(None, requests.get,
                                                    self.used_args.currency_source,
                                                    {'headers': self.used_args.headers})

        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("div", {"class": "valvalue"})
        return convert[0].text

    async def check_currency(self):
        logging.info(self.used_args.log_config)
        logging.info(type(self.used_args.log_config))

        json_data = json.loads(self.used_args.log_config)
        logging.info(json_data)
        logging.basicConfig(filename='log.txt', **json_data)

        while True:
            currency = await self.get_currency_price()
            currency = float(currency.replace(",", "."))
            if currency >= currency + float(self.used_args.tracking_point):
                logging.info("The course has grown a lot! %f", currency)
            elif currency <= currency - float(self.used_args.tracking_point):
                logging.info("The course has dropped a lot! %f", currency)
            logging.info("Current rate: 1 dollar = %f", currency)
            await asyncio.sleep(int(self.used_args.sleep))


async def main():
    while True:
        try:
            start: str = input("Enter command: ")
            if start == "Currency":
                await Currency().check_currency()
            raise ValueError
        except ValueError as err:
            logging.error(err)
            logging.error("Error! Try again?")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="logger.log", filemode="a",
                        format='%(asctime)s %(levelname)s %(message)s')
    asyncio.run(main())
