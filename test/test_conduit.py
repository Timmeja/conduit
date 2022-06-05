# A futtatáshoz használt modulok.
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from def_list import cookie_accept, login
from dict_list import *
from selenium.webdriver.chrome.options import Options



class TestConduit(object):
    # Böngésző definiálása, indítása, oldal megnyitása, ablakbeállítás. Implicit wait használata.
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.browser.implicitly_wait(10)
        URL = 'http://localhost:1667/#/'
        self.browser.get(URL)
        self.browser.maximize_window()

    # Sütik elfogadásának tesztelése, elfogadás után elem eltűnésének asszertálása.
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

    # Címkék listájának bejárása nem regisztrált felhasználóval (nem láthatja a cikkeket).
    # Címke megjelenésének asszertálása az aktuális url-ben.
    def test_make_data_list(self):
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
        # time.sleep(2)
        print('A lista bejárva!')

    # Regisztráció indítása tesztadatok nélkül. Input elemek bejárása TAB segítségével, regisztráció elküldése.
    # Hibaüzenet megjelenésének asszertálása.
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

    # Valid regisztráció létrehozása a teszteléshez. Az adatokat külső dictionary-ben adtam meg.
    def test_user_reg_valid(self):
        cookie_accept(self.browser)
        registration_link = self.browser.find_element_by_xpath('//a[@href="#/register"]')
        registration_link.click()
        reg_username_input = self.browser.find_element_by_xpath('//input[@placeholder="Username"]')
        reg_email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
        reg_password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
        reg_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        reg_username_input.send_keys(user_reg_dict['Username'])
        reg_email_input.send_keys(user_reg_dict['Email'])
        reg_password_input.send_keys(user_reg_dict['Password'])
        reg_btn.click()
        print(user_reg_dict['Email'])
        # Szükséges a time.sleep használata, mert az üzenet szövege megváltozik a feltűnése után ("Now waiting..."),
        # és nekünk a végleges üzenet szövegére van szükségünk.
        time.sleep(2)
        reg_msg = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]'))).text
        print(reg_msg)
        # A többszöri futtatáshoz if-else ágban kezeltem a "Foglalt email" hibaüzenetet.
        try:
            if reg_msg == 'Your registration was successful!':
                print('A regisztráció sikeres')
            elif reg_msg == 'Email already taken.':
                print(
                    'Az email címet már regisztráltuk, megkezdheti a bejelentkezési folyamatot a megadott tesztadatokkal!')
        except AssertionError:
            print('Hiba a regisztráció során')

    # Bejelentkezés előre regisztrált felhasználóval.
    # A főoldal és a bejelentkezés utáni főoldal menüpontmennyiségének asszertálása.
    # (Bejelentkezés után megjelenik a cikkírás, a profilszerkesztés és a saját oldal elérhetősége is.)
    # (Mivel ugyanazok az elemek kerülnek vizsgálatra, szükséges a time.sleep() használata a különbség érzékelhetősége miatt.)
    def test_login(self):
        cookie_accept(self.browser)
        homepage_links = self.browser.find_elements_by_xpath('//li[@class="nav-item"]')
        login_link = self.browser.find_element_by_xpath('//a[@href="#/login"]')
        login_link.click()
        login_email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
        login_email_input.send_keys(login_dict['user'])
        login_password_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
        login_password_input.send_keys(login_dict['password'])
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

    # Oldalak bejárása bejelentkezett felhasználó esetén. Ellenőrzés az érintett lapozó oldalszáma alapján.
    def test_page_list_going_over(self):
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
        time.sleep(2)
        print('Az oldalak bejárva!')

    # Adatmentés az oldalról bejelentkezett felhasználóként. Az adat itt a(z összes felhasználó által) publikált cikkek címének listája.
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
        # Oldal lapozó kód újrafelhasználása.
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
        # Cikkek listába gyűjtése a meglevő 2 oldalról.
        for i in active_page_article_list2:
            article_list.append(i.text)
        # print(article_list)
        # Cikklista kiírása egy külön fájlba.
        with open('../article_list.txt', 'w', encoding='UTF-8') as article_list_text:
            for i in article_list:
                article_list_text.write(i)
                article_list_text.write('\n')

        # Tartalom összehasonlítása az asszertben. A kiírt fájlban egymás alatt jelenítettem meg a címeket,
        # így szükséges a strip() metódus a \n-ek levágásához.
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

    # Új blogposzt felvitele bejelentkezett felhasználóval. Mezők azonosítása, tesztadatok beküldése dictionary felhasználásával.
    # A publikálás megtörténtének ellenőrzése az így keletkező url címmel.
    def test_new_data_input(self):
        cookie_accept(self.browser)
        login(self.browser)
        new_article_link = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
        new_article_link.click()
        article_title_input = self.browser.find_elements_by_xpath('//input[@type="text"]')[0]
        article_title_input.send_keys(new_test_data_dict['title'])
        article_resume = self.browser.find_elements_by_xpath('//input[@type="text"]')[1]
        article_resume.send_keys(new_test_data_dict['resume'])
        article_content = self.browser.find_element_by_xpath('//textarea[@class="form-control"]')
        article_content.send_keys(new_test_data_dict['content'])
        article_tags = self.browser.find_elements_by_xpath('//input[@type="text"]')[2]
        article_tags.send_keys(new_test_data_dict['tag1'], Keys.ENTER, new_test_data_dict['tag2'])
        submit_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')
        submit_btn.click()

        try:
            assert article_title_input.text in self.browser.current_url
            print('A cikk publikálva!')
        except AssertionError:
            print('Hiba a publikálás közben!')

    # Bejelentkezett felhasználó publikációjának módosítása. Ha a felhasználó még nem publikált cikket,
    # az nem módosítható, ezt egy if ággal kezeltem.
    # Ha van saját cikke, abból az elsőt választottam ki módosításra.
    # A tesztadatot txt fájlból olvastatom be, majd töltöm fel az oldalra.
    # A cikk tartalmának asszertálása azonos formátumra hozva azokat (replace metódus segítségével).
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

    # Tesztadatok felvitele a komment szekcióba, majd az összes felvitt kommnet törlése.
    def test_data_fill_and_delete(self):
        cookie_accept(self.browser)
        login(self.browser)
        article_list = self.browser.find_elements_by_xpath('//a[@class="preview-link"]')

        # Az összes cikk listázása után -minden posztot egy új tabon megnyitva- azok alatt
        # egy-egy kommentet helyeztem el.
        for i in range(len(article_list)):
            article_link = article_list[i].get_attribute('href')
            self.browser.execute_script('window.open()')
            time.sleep(1)
            main_tab = self.browser.window_handles[0]
            new_tab = self.browser.window_handles[1]
            self.browser.switch_to.window(new_tab)
            self.browser.get(article_link)
            comment_input = self.browser.find_element_by_xpath('//textarea[@class="form-control"]')
            comment_input.send_keys('Like!')
            post_comment_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-sm btn-primary"]')
            post_comment_btn.click()
            time.sleep(1)
            comment_delete = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//i[@class="ion-trash-a"]')))
            # Assert segítségével ellenőriztem, hogy megjelent-e a komment törlése lehetőség,
            # így bizonyítva, hogy a komment létrejött.
            try:
                assert comment_delete.is_displayed()
                print(f'{i + 1}. komment rögzítve!')
            except AssertionError:
                print(f'Hiba a/az {i + 1}. komment rögzítése közben!')
            self.browser.close()
            self.browser.switch_to.window(main_tab)

        # A cikklistán újra végigiterálva megkerestem az összes, a bejelentkezett felhasználó által írt
        # kommenthez tartozó törlés ikont.
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
            # Amíg a törlés ikonok száma nem nulla (tehát van a bejelentkezett felhasználóhoz tartozó komment),
            # addig folytatódik a kommentek törlése.
            while len(comment_delete) != 0:
                comment_delete[0].click()
                time.sleep(2)
                comment_delete = self.browser.find_elements_by_xpath('//i[@class="ion-trash-a"]')

            # Az asszert alapján, ha a megjelenő komment törlés ikonok száma 0, akkor az összes kommentet törlődött.
            try:
                assert len(comment_delete) == 0
                print(f'{i + 1}. komment törölve!')
            except AssertionError:
                print(f'Hiba a/az {i + 1}. komment törlése közben!')
            self.browser.close()
            self.browser.switch_to.window(main_tab)
            time.sleep(1)

    # Többszörös, sorozatos adatbevitel fájlból, bejelentkezett felhasználóval.
    # Profilkép lecserélése 10 alkalommal fájlban tárolt linkek alapján.
    def test_data_input_from_file(self):
        cookie_accept(self.browser)
        login(self.browser)
        # time.sleep(1)
        settings_link = self.browser.find_element_by_xpath('//a[@href="#/settings"]')
        settings_link.click()
        time.sleep(2)
        # Külső txt fájl beolvasása.
        with open('test/profilkepek.txt', 'r', encoding='UTF-8') as profile_pictures_list:
            list_content = profile_pictures_list.read().split('\n')
        # print(len(list_content))

        # Profilkép inputmezejének azonosítása, előző adat törlése, új képelérhetőség beolvasása fájlból az iterációban.
        # Mivel az elem folyamatosan jelen van, így a WebDriverWait-tel történő várakozás nem hatékony, szükséges a
        # time.sleep használata.
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
            # Szükséges a felugró megerősítő ablakon kívül is ellenőrizni a profilkép változását,
            # hiszen az előbbi csak a link megváltoztatásáról tájékoztat, a kép helyes betöltéséről
            # a felhasználói profilra kattintva győződhetünk meg.
            profile_link = self.browser.find_elements_by_xpath('//li[@class="nav-item"]')[3]
            profile_link.click()
            time.sleep(2)
            user_img = self.browser.find_element_by_xpath('//img[@class="user-img"]').get_attribute('src')
            # # user_img = WebDriverWait(self.browser, 5).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, '//img[@class="user-img"]'))).get_attribute('src')

            # A fájlból betöltött linkek és a megváltozott képek src-je összehasonlítható ellenőrzés céljából.
            try:
                assert i == user_img
                print('A kép megváltozott!')
            except AssertionError:
                print('A kép nem változott!')
            self.browser.back()
            time.sleep(2)

    # Belejentkezett felhasználó kijelentkezése
    def test_logout(self):
        cookie_accept(self.browser)
        login(self.browser)
        time.sleep(2)
        logout_link = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[3]
        logout_link.click()
        time.sleep(2)
        login_link = self.browser.find_element_by_xpath('//a[@href="#/login"]')

        # Ha újra feltűnik a bejelentkezés link, a kijelentkezés sikeres volt.
        try:
            assert login_link.is_displayed()
            print('A kijelentkezés sikeres!')
        except AssertionError:
            print('A kijelentkezés sikertelen!')

    def teardown(self):
        self.browser.quit()
