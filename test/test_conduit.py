import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from def_list import cookie_accept, login
from dict_list import *


class TestConduit(object):
    # Böngésző definiálása, indítása, oldal megnyitása, ablakbeállítás. Implicit wait használata.
    def setup(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(10)
        URL = 'http://localhost:1667/#/'
        self.browser.get(URL)
        self.browser.maximize_window()

    # Sütik elfogadásának tesztelése, elfogadás után elem eltűnésének asszertálása
    def test_cookie_accept(self):
        time.sleep(2)
        cookie_panel = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[@class="cookie cookie__bar cookie__bar--bottom-left"]')))
        cookie_accept = self.browser.find_element_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        cookie_accept.click()
        try:
            cookie_panel = self.browser.find_elements_by_xpath(
                '//div[@class="cookie cookie__bar cookie__bar--bottom-left"]')
            assert len(cookie_panel) == 0
            print('Adatkezelési tájékoztató elfogadva!')
        except AssertionError:
            print('Hiba történt!')


    def teardown(self):
        self.browser.quit()
