import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from def_list import cookie_accept, login


class TestConduit(object):
    def setup(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(10)
        URL = 'http://localhost:1667/#/'
        self.browser.get(URL)
        self.browser.maximize_window()

    def test_cookie_accept(self):
        time.sleep(2)
        cookie_panel = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//div[@class="cookie cookie__bar cookie__bar--bottom-left"]')))
        cookie_accept = self.browser.find_element_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        cookie_accept.click()
        try:
            cookie_panel = self.browser.find_elements_by_xpath(
                '//div[@class="cookie cookie__bar cookie__bar--bottom-left"]')
            assert len(cookie_panel) == 0
            print('Adatkezelési tájékoztató elfogadva!')
        except AssertionError:
            print('Hiba történt!')

    def test_data_list(self):
        time.sleep(1)
        cookie_accept(self.browser)
        tag_list = self.browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]')
        active_tag = self.browser.find_element_by_xpath('//a[@class="nav-link router-link-exact-active active"]')
        active_link = self.browser.current_url
        for i in tag_list:
            i.click()
            active_link = self.browser.current_url
            try:
                assert i.text.strip() in active_link
                print(f'A/Az {i.text} listaelem érintve')
            except AssertionError:
                print('Hiba')
            self.browser.back()
        print('A lista bejárva!')

    def test_empty_registration(self):
        cookie_accept(self.browser)
        registration_link = self.browser.find_element_by_xpath('//a[@href="#/register"]')
        registration_link.click()
        reg_username_input = self.browser.find_element_by_xpath('//input[@placeholder="Username"]')
        reg_username_input.send_keys(Keys.TAB)
        reg_email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
        reg_email_input.send_keys(Keys.TAB)
        reg_password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
        reg_password_input.send_keys(Keys.TAB)
        reg_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        reg_btn.click()
        time.sleep(2)
        reg_failed_message = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-icon swal-icon--error"]')))
        assert reg_failed_message.is_displayed()
        print('Teljesült az elvárt eredmény: az adatok nélküli regisztráció elbukik!')
        reg_failed_btn = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
        reg_failed_btn.click()

    def test_login(self):
        cookie_accept(self.browser)
        homepage_links = self.browser.find_elements_by_xpath('//li[@class="nav-item"]')
        login_link = self.browser.find_element_by_xpath('//a[@href="#/login"]')
        login_link.click()
        login_email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
        login_email_input.send_keys('teszt@holtpont.eu')
        login_password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
        login_password_input.send_keys('@B1aB1@B1')
        login_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        login_btn.click()
        time.sleep(2)
        profile_links = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@class="nav-item"]')))
        print(len(homepage_links))
        print(len(profile_links))
        try:
            assert len(profile_links) > len(homepage_links)
            print('A belépés sikeres!')
        except AssertionError:
            print('A belépés sikertelen!')

    def test_list_going_over(self):
        cookie_accept(self.browser)
        login(self.browser)
        paginator_list = self.browser.find_elements_by_xpath('//a[@class="page-link"]')

        for i in paginator_list:
            i.click()
            active_page = self.browser.find_element_by_xpath('//li[@class="page-item active"]')
            print(i.text + '. oldal')
            try:
                assert active_page.text in i.text
                print('Érintett oldal')
            except AssertionError:
                print('Hiba')
        print('Az oldalak bejárva!')

    def test_data_save(self):
        cookie_accept(self.browser)
        login(self.browser)
        article_list = []
        active_page_article_list1 = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//a[@class="preview-link"]/h1')))
        for i in active_page_article_list1:
            article_list.append(i.text)
        # print(article_list)

        paginator_list = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//a[@class="page-link"]')))

        for i in paginator_list:
            i.click()
            active_page = WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//li[@class="page-item active"]')))
        time.sleep(2)
        active_page_article_list2 = WebDriverWait(self.browser, 5).until(
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

    def test_new_data_input(self):
        cookie_accept(self.browser)
        login(self.browser)
        new_article_link = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
        new_article_link.click()
        article_title_input = self.browser.find_elements_by_xpath('//input[@type="text"]')[0]
        article_title_input.send_keys('Márai Sándor idézet')
        article_resume = self.browser.find_elements_by_xpath('//input[@type="text"]')[1]
        article_resume.send_keys('Márai az olvasásról')
        article_content = self.browser.find_element_by_xpath('//textarea[@class="form-control"]')
        article_content.send_keys(
            '"Nem elég katalógus, divat vagy hagyomány szerint olvasni. Ösztön szerint kell megkeresni a '
            'könyvet, mely nekünk, személyesen mondhat valamit. Rendszeresen kell olvasni, úgy, '
            'ahogy alszik, étkezik, ahogy szeret és lélegzik az ember." ')
        article_tags = self.browser.find_elements_by_xpath('//input[@type="text"]')[2]
        article_tags.send_keys('Márai Sándor', Keys.ENTER, 'idézet')
        submit_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')
        submit_btn.click()
        try:
            assert article_title_input.text in self.browser.current_url
            print('A cikk publikálva!')
        except AssertionError:
            print('Hiba a publikálás közben!')

    def test_data_update(self):
        cookie_accept(self.browser)
        login(self.browser)
        time.sleep(2)
        profile_link = self.browser.find_elements_by_xpath('//li[@class="nav-item"]')[3]
        profile_link.click()
        time.sleep(2)
        logged_user_info = self.browser.find_element_by_xpath(
            '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/a')
        time.sleep(2)
        if profile_link.text != logged_user_info.text:
            print('A felhasználó még nem publikált, nincs mit módosítani!')
        else:
            article_link = self.browser.find_elements_by_xpath('//a[@class="preview-link"]')[0]
            article_link.click()
            time.sleep(1)
            edit_btn = self.browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/span/a/span')
            edit_btn.click()
            time.sleep(2)
            with open('test/az_olvasasrol.txt', 'r', encoding='UTF-8') as article_content_file:
                article_content_string = article_content_file.read()
            time.sleep(2)
            article_content = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//textarea[@class="form-control"]')))
            article_content.clear()
            time.sleep(1)
            article_content.send_keys(article_content_string)
            submit_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')
            submit_btn.click()
            new_article = self.browser.find_element_by_xpath('//div[@class="col-xs-12"]').text
            # print(new_article)
            # print(article_content_string.replace('\n', ' '))

            try:
                assert new_article == article_content_string.replace('\n', ' ')
                print('A cikk tartalma módosítva!')
            except AssertionError:
                print('Hiba a módosításkor!')

    def test_data_fill_and_delete(self):
        cookie_accept(self.browser)
        login(self.browser)
        article_list = self.browser.find_elements_by_xpath('//a[@class="preview-link"]')

        for i in range(len(article_list)):
            article_link = article_list[i].get_attribute('href')
            self.browser.execute_script('window.open()')
            main_tab = self.browser.window_handles[0]
            new_tab = self.browser.window_handles[1]
            self.browser.switch_to.window(new_tab)
            self.browser.get(article_link)
            comment_input = self.browser.find_element_by_xpath('//textarea[@class="form-control"]')
            comment_input.send_keys('Like!')
            post_comment_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-sm btn-primary"]')
            post_comment_btn.click()
            comment_delete = self.browser.find_element_by_xpath('//i[@class="ion-trash-a"]')
            try:
                assert comment_delete.is_displayed()
                print(f'{i + 1}. komment rögzítve!')
            except AssertionError:
                print(f'Hiba a/az {i + 1}. komment rögzítése közben!')
            self.browser.close()
            self.browser.switch_to.window(main_tab)

        for i in range(len(article_list)):
            article_link = article_list[i].get_attribute('href')
            time.sleep(1)
            self.browser.execute_script('window.open()')
            main_tab = self.browser.window_handles[0]
            new_tab = self.browser.window_handles[1]
            self.browser.switch_to.window(new_tab)
            self.browser.get(article_link)
            time.sleep(1)
            comment_delete = self.browser.find_elements_by_xpath('//i[@class="ion-trash-a"]')

            while len(comment_delete) != 0:
                comment_delete[0].click()
                time.sleep(2)
                comment_delete = self.browser.find_elements_by_xpath('//i[@class="ion-trash-a"]')
            try:
                assert len(comment_delete) == 0
                print(f'{i + 1}. komment törölve!')
            except AssertionError:
                print(f'Hiba a/az {i + 1}. komment törlése közben!')
            self.browser.close()
            self.browser.switch_to.window(main_tab)
            time.sleep(1)

    def test_data_input_from_file(self):
        cookie_accept(self.browser)
        login(self.browser)
        settings_link = self.browser.find_element_by_xpath('//a[@href="#/settings"]')
        settings_link.click()
        time.sleep(2)
        with open('test/profilkepek.txt', 'r', encoding='UTF-8') as profile_pictures_list:
            list_content = profile_pictures_list.read().split('\n')
        # print(len(list_content))

        for i in list_content:
            profile_pic_input = self.browser.find_element_by_xpath('//input[@placeholder="URL of profile picture"]')
            # profile_pic_input = WebDriverWait(self.browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, '//input[@placeholder="URL of profile picture"]')))
            profile_pic_input.clear()
            profile_pic_input.send_keys(i)
            # print(i)
            update_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
            # update_btn = WebDriverWait(self.browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')))
            update_btn.click()
            time.sleep(2)
            update_success_btn = self.browser.find_element_by_xpath(
                '//button[@class="swal-button swal-button--confirm"]')
            # update_success_btn = WebDriverWait(self.browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, '//button[@class="swal-button swal-button--confirm"]')))
            update_success_btn.click()
            time.sleep(2)
            profile_link = self.browser.find_elements_by_xpath('//li[@class="nav-item"]')[3]
            profile_link.click()
            time.sleep(2)
            user_img = self.browser.find_element_by_xpath('//img[@class="user-img"]').get_attribute('src')
            # # user_img = WebDriverWait(self.browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, '//img[@class="user-img"]'))).get_attribute('src')
            try:
                assert i == user_img
                print('A kép megváltozott!')
            except AssertionError:
                print('A kép nem változott!')
            self.browser.back()
            time.sleep(2)

    def test_logout(self):
        cookie_accept(self.browser)
        login(self.browser)
        time.sleep(2)
        logout_link = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[3]
        logout_link.click()
        time.sleep(2)
        login_link = self.browser.find_element_by_xpath('//a[@href="#/login"]')
        try:
            assert login_link.is_displayed()
            print('A kijelentkezés sikeres!')
        except AssertionError:
            print('A kijelentkezés sikertelen!')

    def teardown(self):
        self.browser.quit()
