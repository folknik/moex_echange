import os
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


token = os.environ['token']
chat_id = os.environ['çhat_id']


class WebOptions(object):
    def init(self):
        self.options = Options()
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('headless')
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--remote-debugin-port=9222")
        self.options.add_argument("--screen-size=1200x800")

    @property
    def extract(self):
        return self.options


def bot_sendtext(message):
    text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&text=' + message
    requests.get(text)


def get_price(stock):
    pass


if __name__ == '__main__':
    stocks = [
        ['GAZP', 'https://ru.investing.com/equities/gazprom_rts', 'RUB'],
        ['AFLT', 'https://ru.investing.com/equities/aeroflot', 'RUB']
    ]
    webdriver.Chrome(executable_path='your_path_to_chromdriver', options=WebOptions().extract)
    try:
        for stock in stocks:
            get_price(stock)
    except KeyboardInterrupt:
        webdriver.close()

