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
