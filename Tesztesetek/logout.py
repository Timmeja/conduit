import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(10)
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

login_link = browser.find_element_by_xpath('//a[@href="#/login"]')
login_link.click()
login_email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
login_email_input.send_keys('teszt@holtpont.eu')
login_password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
login_password_input.send_keys('@B1aB1@B1')
login_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
login_btn.click()
time.sleep(2)

logout_link = browser.find_elements_by_xpath('//a[@class="nav-link"]')[3]
logout_link.click()
time.sleep(2)
try:
    assert login_link.is_displayed()
    print('A kijelentkezés sikeres!')
except AssertionError:
    print('A kijelentkezés sikertelen!')

browser.quit()
