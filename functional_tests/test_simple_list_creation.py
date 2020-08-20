from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

    
class NewVisitorTest(FunctionalTest):
    """Тест для нового посетителя"""
    
    def test_can_start_a_list_for_one_user(self):
        """Тест: можно начать список и получить его позже"""
        
        # Эрнест где-то услыхал, что списки дел экономят психическую энергию
        # которой ему маловато в последнее время
        # Он решил оценить домашнюю страницу такого приложения
        self.browser.get(self.live_server_url)

        # Он обращает внимание, что заголовок и шапка страницы намекают на список дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ему предлагают ввести в список дело, которым нельзя пренебречь
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        # В текстовом поле Эрнест пишет "Привести себя в порядок"
        # Ведь в последнее время он много пил и пренебрегал бритьём
        inputbox.send_keys('Привести себя в порядок')
        
        # Когда он нажимает enter - страница обновляется и теперь страница
        # содержит "1: Привести себя в порядок" в качестве элемента
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table('1: Привести себя в порядок')
        # Текстовое поле по-прежнему приглашает Эрнеста сделать запись 
        # Что ж, пора "Убрать весь хлам на кухне"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Убрать весь хлам на кухне')
        inputbox.send_keys(Keys.ENTER)
        
        # Страница снова обновляется и теперь показывает оба элемента списка
        self.wait_for_row_in_list_table("1: Привести себя в порядок")
        self.wait_for_row_in_list_table("2: Убрать весь хлам на кухне")
        # Удовлетворённый своими "амбициозными планами", Эрнест снова засыпает
        
    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Тест: многочисленные пользователи могут начать списки по разным url"""
        
        # Эрнест начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Привести себя в порядок')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Привести себя в порядок')
        
        # Он замечает, что его список имеет уникальный URL-адрес
        ernest_list_url = self.browser.current_url
        self.assertRegex(ernest_list_url, '/lists/.+')
        self.browser.quit()
        
        ### Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ### информация от Эрнеста не прошла через данные cookie и пр.
        
        # Теперь новый пользователь Флавий приходит на сайт
        self.browser = webdriver.Firefox()
        
        # Флавий посещает домашнюю страницу и нет никаких признаков списка Эрнеста
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Привести себя в порядок', page_text)
        self.assertNotIn('Убрать весь хлам на кухне', page_text)
        
        # Флавий начинает новый список, вводя новый элемент. Его список не менее
        # интересен, чем у Эрнеста
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Разбить варваров на севере Британии')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Разбить варваров на севере Британии')
        
        # Флавий получает уникальный URL-адрес
        flawiy_list_url = self.browser.current_url
        self.assertRegex(flawiy_list_url, '/lists/(.+)')
        self.assertNotEqual(flawiy_list_url, ernest_list_url)
        
        # Опять таки нет ни следа от списка Эрнеста
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Привести себя в порядок', page_text)
        self.assertIn('Разбить варваров на севере Британии', page_text)