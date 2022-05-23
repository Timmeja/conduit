from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

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

new_article_link = browser.find_element_by_xpath('//a[@href="#/editor"]')
new_article_link.click()

article_title_input = browser.find_elements_by_xpath('//input[@type="text"]')[0]
article_title_input.send_keys('Márai Sándor idézet')
article_resume = browser.find_elements_by_xpath('//input[@type="text"]')[1]
article_resume.send_keys('Márai az olvasásról')
article_content = browser.find_element_by_xpath('//textarea[@class="form-control"]')
article_content.send_keys('"Nem elég katalógus, divat vagy hagyomány szerint olvasni. Ösztön szerint kell megkeresni a '
                          'könyvet, mely nekünk, személyesen mondhat valamit. Rendszeresen kell olvasni, úgy, '
                          'ahogy alszik, étkezik, ahogy szeret és lélegzik az ember." ')
article_tags = browser.find_elements_by_xpath('//input[@type="text"]')[2]
article_tags.send_keys('Márai Sándor', Keys.ENTER, 'idézet')

submit_btn = browser.find_element_by_xpath('//button[@type="submit"]')
submit_btn.click()

try:
    assert article_title_input.text in browser.current_url
    print('A cikk publikálva!')
except AssertionError:
    print('Hiba a publikálás közben!')

browser.quit()
