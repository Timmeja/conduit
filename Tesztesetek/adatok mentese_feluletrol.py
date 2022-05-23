import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from def_list import cookie_accept, login

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(10)
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

cookie_accept(browser)
login(browser)
article_list = []
active_page_article_list1 = WebDriverWait(browser, 5).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//a[@class="preview-link"]/h1')))
for i in active_page_article_list1:
    article_list.append(i.text)
# print(article_list)

paginator_list = WebDriverWait(browser, 5).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//a[@class="page-link"]')))

for i in paginator_list:
    i.click()
    active_page = WebDriverWait(browser, 5).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//li[@class="page-item active"]')))
time.sleep(2)
active_page_article_list2 = WebDriverWait(browser, 5).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//a[@class="preview-link"]/h1')))

for i in active_page_article_list2:
    article_list.append(i.text)
# print(article_list)

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
