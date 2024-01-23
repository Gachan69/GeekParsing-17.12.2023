from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    url = 'https://habr.com/ru'
    browser = webdriver.Chrome()
    browser.get(url)
    print(1)