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

settings_link = browser.find_element_by_xpath('//a[@href="#/settings"]')
settings_link.click()

with open('../test/profilkepek.txt', 'r', encoding='UTF-8') as profile_pictures_list:
    list_content = profile_pictures_list.read().split('\n')
# print(len(list_content))

for i in list_content:
    profile_pic_input = browser.find_element_by_xpath('//input[@placeholder="URL of profile picture"]')
    profile_pic_input.clear()
    profile_pic_input.send_keys(i)
    # print(i)
    update_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    update_btn.click()
    update_success_btn = browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
    update_success_btn.click()
    time.sleep(1)
    profile_link = browser.find_elements_by_xpath('//li[@class="nav-item"]')[3]
    profile_link.click()
    time.sleep(2)
    user_img = browser.find_element_by_xpath('//img[@class="user-img"]').get_attribute('src')
    try:
        assert i == user_img
        print('A kép megváltozott!')
    except AssertionError:
        print('A kép nem változott!')
    browser.back()

browser.quit()
