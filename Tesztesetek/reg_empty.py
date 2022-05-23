from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from def_list import cookie_accept

browser = webdriver.Chrome(ChromeDriverManager().install())
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

cookie_accept(browser)
registration_link = browser.find_element_by_xpath('//a[@href="#/register"]')
registration_link.click()
reg_username_input = browser.find_element_by_xpath('//input[@placeholder="Username"]')
reg_username_input.send_keys(Keys.TAB)
reg_email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
reg_email_input.send_keys(Keys.TAB)
reg_password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
reg_password_input.send_keys(Keys.TAB)
reg_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
reg_btn.click()

reg_failed_message = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="swal-icon swal-icon--error"]')))

assert reg_failed_message.is_displayed()
print('Teljesült az elvárt eredmény: az adatok nélküli regisztráció elbukik!')

reg_failed_btn = browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
reg_failed_btn.click()

browser.quit()
