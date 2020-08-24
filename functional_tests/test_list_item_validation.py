from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip


class ItemValidationTest(FunctionalTest):
    """Тест валидации элементов списка"""
    
    def test_cannot_add_empty_list_items(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        # Эрнест открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # Браузер перехватывает запрос и не загружает странциу со списком
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'))
        
        # Теперь Эрнест уже пробует по-нормальному что-то добавить
        self.get_item_input_box().send_keys('Scratch a turnip')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'))
        
        # и может отправить форму успешно
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Scratch a turnip')
        
        # Каким бы странным это не казалось, он пытается
        # повторить трюк с пустым полем
        self.get_item_input_box().send_keys(Keys.ENTER)
        
        # Результат такой же
        self.wait_for_row_in_list_table('1: Scratch a turnip')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'))
        
        # И он может исправить его, заполнив нейким текстом
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Scratch a turnip')
        self.wait_for_row_in_list_table('2: Make tea')
        
        self.fail('End test!')