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
profile_link = browser.find_elements_by_xpath('//li[@class="nav-item"]')[3]
profile_link.click()
time.sleep(2)
article_link = browser.find_elements_by_xpath('//a[@class="preview-link"]')[0]
article_link.click()

edit_btn = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/span/a/span')
edit_btn.click()

with open('../test/az_olvasasrol.txt', 'r', encoding='UTF-8') as article_content_file:
    article_content_string = article_content_file.read()

article_content = browser.find_element_by_xpath('//textarea[@class="form-control"]')
article_content.clear()
article_content.send_keys(article_content_string)


submit_btn = browser.find_element_by_xpath('//button[@type="submit"]')
submit_btn.click()

new_article = browser.find_element_by_xpath('//div[@class="col-xs-12"]').text
# print(new_article)
# print(article_content_string.replace('\n', ' '))

try:
    assert new_article == article_content_string.replace('\n', ' ')
    print('A cikk tartalma módosítva!')
except AssertionError:
    print('Hiba a módosításkor!')

browser.quit()

