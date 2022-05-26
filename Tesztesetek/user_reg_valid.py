import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from def_list import cookie_accept
from dict_list import *

browser = webdriver.Chrome(ChromeDriverManager().install())
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

cookie_accept(browser)
registration_link = browser.find_element_by_xpath('//a[@href="#/register"]')
registration_link.click()

reg_username_input = browser.find_element_by_xpath('//input[@placeholder="Username"]')
reg_email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
reg_password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
reg_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')

reg_username_input.send_keys(user_reg_dict['Username'])
reg_email_input.send_keys(user_reg_dict['Email'])
reg_password_input.send_keys(user_reg_dict['Password'])
reg_btn.click()
print(user_reg_dict['Email'])
time.sleep(2)
reg_msg = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]'))).text
print(reg_msg)
try:
    if reg_msg == 'Your registration was successful!':
        print('A regisztráció sikeres')
    elif reg_msg == 'Email already taken.':
        print('Az email címet már regisztráltuk, megkezdheti a bejelentkezési folyamatot a megadott tesztadatokkal!')
except AssertionError:
    print('Hiba a regisztráció során')

browser.quit()