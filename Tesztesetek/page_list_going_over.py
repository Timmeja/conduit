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
paginator_list = browser.find_elements_by_xpath('//a[@class="page-link"]')

for i in paginator_list:
    i.click()
    active_page = browser.find_element_by_xpath('//li[@class="page-item active"]')
    print(i.text + '. oldal')
    try:
        assert active_page.text in i.text
        print('Érintett oldal')
    except AssertionError:
        print('Hiba')
print('Az oldalak bejárva!')

browser.quit()
