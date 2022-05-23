from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(10)
URL = 'http://localhost:1667/#/'
browser.get(URL)
browser.maximize_window()

tag_list = browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]')
active_tag = browser.find_element_by_xpath('//a[@class="nav-link router-link-exact-active active"]')
active_link = browser.current_url

for i in tag_list:
    i.click()
    active_link = browser.current_url

    try:
        assert i.text.strip() in active_link
        print(f'A/Az {i.text} listaelem érintve')
    except AssertionError:
        print('Hiba')
    browser.back()
print('A lista bejárva!')

browser.quit()
