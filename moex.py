import sys
import requests
from time import sleep
from datetime import datetime, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


token = sys.argv[1]
chat_id = sys.argv[2]

SLEEP_MINUTES = 10
START_SESSION = time(10, 0, 0)
END_SESSION = time(18, 45, 0)


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


def bot_sendtext(message):
    text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&text=' + message
    requests.get(text)


def get_price(driver, link):
    driver.get(link)
    price = driver.find_element_by_xpath("//*[@id='last_last']").text.replace(',', '.')
    percent = float(driver.find_element_by_xpath("//*[@id='quotes_summary_current_data']/div[1]/div[2]/div[1]/span[4]").text.replace(',', '.').replace('%', ''))
    return price, percent


if __name__ == '__main__':
    stocks = [
        ['GAZP', 'https://ru.investing.com/equities/gazprom_rts', 'RUB'],
        ['TATN', 'https://ru.investing.com/equities/tatneft_rts', 'RUB'],
        ['SBER', 'https://ru.investing.com/equities/sberbank_rts', 'RUB'],
        ['GMKN', 'https://ru.investing.com/equities/gmk-noril-nickel_rts', 'RUB'],
        ['AFLT', 'https://ru.investing.com/equities/aeroflot', 'RUB'],
    ]
    options = WebOptions().extract
    driver = webdriver.Chrome(executable_path='/Users/afadeev/Documents/chromedriver', options=options)
    while True:
        try:
            if datetime.today().weekday() < 5 and START_SESSION <= datetime.now().time() <= END_SESSION:
                stock_prices = [get_price(driver, stock[1]) for stock in stocks]
                message_list = [(s[0], p[0], s[2], p[1]) for p, s in zip(stock_prices, stocks)]
                message_list = sorted(message_list, key=lambda x: x[3], reverse=True)
                messages = ["{}: {} {}, {}%".format(m[0], m[1], m[2], m[3]) for m in message_list]
                bot_sendtext("\n".join(messages))
                sleep(60 * SLEEP_MINUTES)
        except KeyboardInterrupt:
            driver.close()