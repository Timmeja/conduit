import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from def_list import cookie_accept, login

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(10)
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

cookie_accept(browser)
login(browser)
time.sleep(2)
logout_link = browser.find_elements_by_xpath('//a[@class="nav-link"]')[3]
logout_link.click()
time.sleep(2)
login_link = browser.find_element_by_xpath('//a[@href="#/login"]')
try:
    assert login_link.is_displayed()
    print('A kijelentkezés sikeres!')
except AssertionError:
    print('A kijelentkezés sikertelen!')

browser.quit()
