from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def cookie_accept(b):
    cookie_panel = WebDriverWait(b, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="cookie cookie__bar cookie__bar--bottom-left"]')))
    cookie_accept = b.find_element_by_xpath(
        '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    cookie_accept.click()


def login(b):
    login_link = b.find_element_by_xpath('//a[@href="#/login"]')
    login_link.click()
    login_email_input = b.find_element_by_xpath('//input[@placeholder="Email"]')
    login_email_input.send_keys('teszt@holtpont.eu')
    login_password_input = b.find_element_by_xpath('//input[@placeholder="Password"]')
    login_password_input.send_keys('@B1aB1@B1')
    login_btn = b.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    login_btn.click()