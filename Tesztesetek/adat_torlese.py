import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(2)
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

article_list = browser.find_elements_by_xpath('//a[@class="preview-link"]')

for i in range(len(article_list)):
    article_link = article_list[i].get_attribute('href')
    browser.execute_script('window.open()')
    main_tab = browser.window_handles[0]
    new_tab = browser.window_handles[1]
    browser.switch_to.window(new_tab)
    browser.get(article_link)
    comment_input = browser.find_element_by_xpath('//textarea[@class="form-control"]')
    comment_input.send_keys('Like!')
    post_comment_btn = browser.find_element_by_xpath('//button[@class="btn btn-sm btn-primary"]')
    post_comment_btn.click()
    comment_delete = browser.find_element_by_xpath('//i[@class="ion-trash-a"]')
    try:
        assert comment_delete.is_displayed()
        print(f'{i + 1}. komment rögzítve!')
    except AssertionError:
        print(f'Hiba a/az {i + 1}. komment rögzítése közben!')
    browser.close()
    browser.switch_to.window(main_tab)

for i in range(len(article_list)):
    article_link = article_list[i].get_attribute('href')
    time.sleep(1)
    browser.execute_script('window.open()')
    main_tab = browser.window_handles[0]
    new_tab = browser.window_handles[1]
    browser.switch_to.window(new_tab)
    browser.get(article_link)
    time.sleep(1)
    comment_delete = browser.find_elements_by_xpath('//i[@class="ion-trash-a"]')

    while len(comment_delete) != 0:
        comment_delete[0].click()
        time.sleep(2)
        comment_delete = browser.find_elements_by_xpath('//i[@class="ion-trash-a"]')
    try:
        assert len(comment_delete) == 0
        print(f'{i + 1}. komment törölve!')
    except AssertionError:
        print(f'Hiba a/az {i + 1}. komment törlése közben!')
    browser.close()
    browser.switch_to.window(main_tab)

browser.quit()
