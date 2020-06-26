import os
import sys
import datetime
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')


def login(driver ,email, password):
    url = 'https://ssl.syosetu.com/login/input/'
    print(datetime.datetime.now().isoformat(), 'GET:', url)

    driver.get(url)

    id_elem = driver.find_element_by_css_selector('input[name="narouid"]')
    id_elem.send_keys(email)

    pass_elem = driver.find_element_by_css_selector('input[name="pass"]')
    pass_elem.send_keys(password)

    driver.find_element_by_css_selector('#mainsubmit').click()


if __name__ == '__main__':
    email = os.getenv('NAROU_EMAIL')
    password = os.getenv('NAROU_PASSWORED')

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    # Login
    login(driver, email, password)

    # Capture
    file_path = os.path.join(ROOT_PATH, 'tmp', 'capture.png')
    driver.save_screenshot(file_path)

