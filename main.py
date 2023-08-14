import configargparse #imports the configargparse module, which is used to parse command line arguments from a configuration file.
import asyncio #imports the asyncio module, which provides tools for writing asynchronous code.
import requests #imports the requests module, which is used to send HTTP requests.
from bs4 import BeautifulSoup #imports the BeautifulSoup class from the bs4 module, which is used to parse HTML code.
import logging #imports the logging module, which is used for event logging.
import json #imports the json module, which is used to work with JSON data.

class ParseIni: #defines the ParseIni class, which is used to parse the configuration file.
    def __init__(self): #defines a constructor for the ParseIni class.
        parser = configargparse.ArgParser() #creates an instance of the ArgParser class from the configargparse module that will be used to parse command line arguments.
        parser.add_argument('-c, --config', required=True, is_config_file=True, help='Path to file config.ini') #adds the -c or --config command line argument, which is required and specifies the path to the config.ini configuration file.
        parser.add_argument('--currency_source', default='http://www.finmarket.ru/currency/USD/',
                            help='Currency web-source') #adds the --currency_source command line argument, which has the default value http://www.finmarket.ru/currency/USD/ and specifies the source of the currency rate data.
        parser.add_argument('--sleep', default=3, help='Update delay in seconds') #adds the --sleep command line argument, which has a default value of 3 and specifies the refresh delay in seconds.
        parser.add_argument('--tracking_point', default=0.5, help='Change rate point') #adds the --tracking_point command line argument, which has a default value of 0.5 and specifies the change point for the currency rate.
        parser.add_argument('--headers', default={'User-Agent': 'Mozilla/5.0'}, help='Change rate point') #adds the --headers command line argument, which defaults to {'User-Agent': 'Mozilla/5.0'} and specifies the HTTP request headers.
        parser.add_argument('--log_config', default={"level": logging.INFO,
                                                     "format": '%(asctime)s %(levelname)s %(message)s'},
                            help='Log configs') #adds the --log_config command line argument, which defaults to {"level": logging.INFO, "format": '%(asctime)s %(levelname)s %(message)s'} and specifies the event log configuration.
        args = parser.parse_args() #parses the command line arguments and stores the results in the args variable.
        self.currency_source = args.currency_source #stores the value of the currency_source argument in the currency_source attribute of an instance of the ParseIni class.
        self.sleep = args.sleep #stores the value of the sleep argument in the sleep attribute of the ParseIni instance.
        self.tracking_point = args.tracking_point #stores the value of the tracking_point argument in the tracking_point attribute of an instance of the ParseIni class.
        self.headers = args.headers #stores the value of the headers argument in the headers attribute of an instance of the ParseIni class.
        self.log_config = args.log_config #stores the value of the log_config argument in the log_config attribute of an instance of the ParseIni class.


class Currency: #defines the Currency class, which is used to work with the currency rate.
    used_args = ParseIni() #creates an instance of the ParseIni class and stores it in the variable used_args.

    def __init__(self): #defines a constructor for the Currency class.
        self.loop = asyncio.get_event_loop() #creates an event loop using the get_event_loop() function from the asyncio module.

    async def get_currency_price(self): #defines an asynchronous get_currency_price function that is used to get the current currency rate.
        full_page = await self.loop.run_in_executor(None, requests.get, self.used_args.currency_source,
                                                    {'headers': self.used_args.headers}) #makes an asynchronous call to the requests.get function using the run_in_executor method of the loop event loop to get the full page using an HTTP request.

        soup = BeautifulSoup(full_page.content, 'html.parser') #creates a BeautifulSoup object to parse the page's HTML code.
        convert = soup.findAll("div", {"class": "valvalue"}) #finds all <div> elements with class valvalue on the page.
        return convert[0].text #returns the text of the first element found.

    async def check_currency(self): #defines an asynchronous check_currency function that is used to check the currency rate.
        print(self.used_args.log_config) #displays the value of the log_config attribute of an instance of the ParseIni class.
        print(type(self.used_args.log_config)) #infers the type of the value of the log_config attribute of an instance of the ParseIni class.
        # logging.basicConfig(filename='log.txt', **self.used_args.log_config)

        jsonData = json.loads(self.used_args.log_config) #converts the log_config attribute value in JSON format to a Python object.
        print(jsonData) #outputs the converted Python object.
        logging.basicConfig(filename='log.txt', **jsonData) #configures the event log using the basicConfig function from the logging module and passes arguments from the jsonData object.

        while True:
            currency = await self.get_currency_price() #calls the asynchronous get_currency_price function to get the current currency rate.
            currency = float(currency.replace(",", ".")) #converts the string currency to a floating point number, replacing the comma with a dot.
            if currency >= currency + float(self.used_args.tracking_point): #Checks for changes in the exchange rate and writes appropriate messages to the event log and displays them on the screen.
                logging.info("The course has grown a lot!")
                print(f"The course has grown a lot! {currency}")
            elif currency <= currency - float(self.used_args.tracking_point):
                logging.info("The course has dropped a lot!")
                print(f"The course has dropped a lot! {currency}")
            logging.info(f"Current rate: 1 dollar = {currency}") #writes a message about the current exchange rate to the event log.
            print(f"Current rate: 1 dollar = {currency}") #displays a message about the current exchange rate on the screen.
            await asyncio.sleep(int(self.used_args.sleep)) #pauses program execution for the specified number of seconds.


async def main(): #defines an asynchronous main function, which is the entry point to the program.
    while True: #endless cycle.
        try:
            start: str = input("Enter command: ") #prompts the user for a command.
            if start == "Currency": #checks if the entered command is equal to "Currency", then the next line is executed.
                await Currency().check_currency() #creates an instance of the Currency class and calls the check_currency() method.
            raise ValueError #throws a ValueError exception.
        except ValueError as err: #This block of code handles the ValueError exception, displays an error message, and prompts you to try again.
            print(err)
            print("Error! Try again?")


if __name__ == "__main__": #checks if the module is being executed as the main program, then the next block of code is executed.
    asyncio.run(main())
