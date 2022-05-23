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

article_list = []
active_page_article_list1 = browser.find_elements_by_xpath('//a[@class="preview-link"]/h1')
for i in active_page_article_list1:
    article_list.append(i.text)
paginator_list = browser.find_elements_by_xpath('//a[@class="page-link"]')

for i in paginator_list:
    i.click()
    active_page = browser.find_element_by_xpath('//li[@class="page-item active"]')
time.sleep(1)
active_page_article_list2 = browser.find_elements_by_xpath('//a[@class="preview-link"]/h1')

for i in active_page_article_list2:
    article_list.append(i.text)

with open('../article_list.txt', 'w', encoding='UTF-8') as article_list_text:
    for i in article_list:
        article_list_text.write(i)
        article_list_text.write('\n')

try:
    with open('../article_list.txt', 'r', encoding='UTF-8') as assert_file:
        text_content = assert_file.readlines()
        text_content_assert = []
        for i in text_content:
            text_content_assert.append(i.strip())
        # print(text_content_assert)
        # print(article_list)
    assert text_content_assert == article_list
    print('Az adatmentés sikeres!')
except FileNotFoundError:
    print('Az adatmentés sikertelen volt!')

browser.quit()
