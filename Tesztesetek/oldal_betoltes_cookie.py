from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome(ChromeDriverManager().install())
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

def cookie_accept():
    cookie_panel = WebDriverWait(browser, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="cookie cookie__bar cookie__bar--bottom-left"]')))
    cookie_accept = browser.find_element_by_xpath(
        '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
    cookie_accept.click()

cookie_accept()
try:
    cookie_panel = browser.find_elements_by_xpath('//div[@class="cookie cookie__bar cookie__bar--bottom-left"]')
    assert len(cookie_panel) == 0
    print('Adatkezelési tájékoztató elfogadva!')
except AssertionError:
    print('Hiba történt!')

browser.quit()
