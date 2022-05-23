import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome(ChromeDriverManager().install())
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

def login():
    login_link = browser.find_element_by_xpath('//a[@href="#/login"]')
    login_link.click()
    login_email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    login_email_input.send_keys('teszt@holtpont.eu')
    login_password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
    login_password_input.send_keys('@B1aB1@B1')
    login_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    login_btn.click()



login()
homepage_links = browser.find_elements_by_xpath('//li[@class="nav-item"]')
time.sleep(2)
profile_links = WebDriverWait(browser, 5).until(
    EC.presence_of_all_elements_located((By.XPATH, '//li[@class="nav-item"]')))
print(len(homepage_links))
print(len(profile_links))
try:
    assert len(profile_links) > len(homepage_links)
    print('A belépés sikeres!')
except AssertionError:
    print('A belépés sikertelen!')

browser.quit()
