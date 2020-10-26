import json
import requests
import numpy as np
from time import sleep
from datetime import datetime, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


with open("./credentials.json", "r+") as file:
    cred = json.loads(file.read())


class WebOptions(object):
    def __init__(self):
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


class MOEX(object):
    def __init__(self, chromedriver_path, options, stocks):
        self.options = options
        self.chromedriver_path = chromedriver_path
        self.stocks = stocks
        self.driver = None
        self.start = time(10, 0, 0)
        self.end = time(18, 45, 0)
        self.price_xpath = "//*[@id='last_last']"
        self.percent_xpath = "//*[@id='quotes_summary_current_data']/div[1]/div[2]/div[1]/span[4]"
        # self.volume_xpath = "//*[@id='quotes_summary_secondary_data']/div/ul/li[1]/span[2]/span"

    def get_price(self, link):
        self.driver.get(link)
        price = self.driver.find_element_by_xpath(self.price_xpath).text.replace(',', '.')
        percent = float(self.driver.find_element_by_xpath(self.percent_xpath).text.replace(',', '.').replace('%', ''))
        return price, percent

    def get_price_list(self):
        links = [stock[1] for stock in self.stocks]
        prices = [self.get_price(link) for link, stock in zip(links, self.stocks)]
        return prices

    def run(self):
        if datetime.today().weekday() < 5 and self.start <= datetime.now().time() <= self.end:
            prices = self.get_price_list()

            # make message like Сбербанк: 213.10 RUB, -0.65%
            message_list = [(s[3], p[0], s[2], p[1]) for p, s in zip(prices, stocks)]

            # sorted by percent
            message_list = np.array(sorted(message_list, key=lambda x: x[3], reverse=True))

            oil = message_list[message_list[:, 0] == 'Нефть Brent']
            no_oil = message_list[message_list[:, 0] != 'Нефть Brent']
            message_list = np.vstack((oil, no_oil))

            message = ["{}: {} {}, {}%".format(m[0], m[1], m[2], m[3]) for m in message_list]
            MOEX.send_message("\n".join(message))
            print("Message was sent, {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    @staticmethod
    def send_message(message):
        text = 'https://api.telegram.org/bot' + cred['token'] \
               + '/sendMessage?chat_id=' + cred['chat_id'] + '&text=' + message
        requests.get(text)

    def __enter__(self):
        print("MOEX echange started")
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, options=self.options)
        return self

    def __exit__(self):
        self.driver.close()


if __name__ == '__main__':
    stocks = [
        ['BF1', 'https://ru.investing.com/commodities/brent-oil', 'USD', 'Нефть Brent'],
        ['GAZP', 'https://ru.investing.com/equities/gazprom_rts', 'RUB', 'Газпром'],
        ['TATN', 'https://ru.investing.com/equities/tatneft_rts', 'RUB', 'Татнефть'],
        ['SBER', 'https://ru.investing.com/equities/sberbank_rts', 'RUB', 'Сбербанк'],
        ['GMKN', 'https://ru.investing.com/equities/gmk-noril-nickel_rts', 'RUB', 'Норникель'],
        ['AFLT', 'https://ru.investing.com/equities/aeroflot', 'RUB', 'Аэрофлот'],
        ['YNDX', 'https://ru.investing.com/equities/yandex?cid=102063', 'RUB', 'Яндекс'],
        ['NLMK', 'https://ru.investing.com/equities/nlmk_rts', 'RUB', 'НЛМК'],
        ['MVID', 'https://ru.investing.com/equities/mvideo_rts', 'RUB', 'М.Видео'],
        ['LNTADR', 'https://ru.investing.com/equities/lenta-ltd?cid=962408', 'RUB', 'Lenta Ltd']
    ]
    SLEEP_MINUTES = 10
    options = WebOptions().extract
    with MOEX(cred['chromedriver_path'], options, stocks) as exchange:
        while True:
            exchange.run()
            sleep(60 * SLEEP_MINUTES)