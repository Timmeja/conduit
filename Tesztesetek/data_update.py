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
time.sleep(2)
profile_link = browser.find_elements_by_xpath('//li[@class="nav-item"]')[3]
profile_link.click()
time.sleep(2)
logged_user_info = browser.find_element_by_xpath(
    '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/a')
time.sleep(2)
if profile_link.text != logged_user_info.text:
    print('A felhasználó még nem publikált, nincs mit módosítani!')
else:
    article_link = browser.find_elements_by_xpath('//a[@class="preview-link"]')[0]
    article_link.click()
    time.sleep(1)
    edit_btn = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/span/a/span')
    edit_btn.click()
    with open('az_olvasasrol.txt', 'r', encoding='UTF-8') as article_content_file:
        article_content_string = article_content_file.read()
    time.sleep(2)
    article_content = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, '//textarea[@class="form-control"]')))
    article_content.clear()
    time.sleep(1)
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
