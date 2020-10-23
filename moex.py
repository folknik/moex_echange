import sys
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


token = sys.argv[1]
chat_id = sys.argv[2]


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
    price = driver.find_element_by_xpath("//*[@id='last_last']").text
    return price


if __name__ == '__main__':
    stocks = [
        ['GAZP', 'https://ru.investing.com/equities/gazprom_rts', 'RUB'],
        ['AFLT', 'https://ru.investing.com/equities/aeroflot', 'RUB']
    ]
    options = WebOptions().extract
    driver = webdriver.Chrome(executable_path='/Users/afadeev/Documents/chromedriver', options=options)
    while True:
        try:
            for stock in stocks:
                price = get_price(driver, stock[1])
                print(stock[0], price)
                bot_sendtext(stock[0])
            sleep(60)
        except KeyboardInterrupt:
            driver.close()