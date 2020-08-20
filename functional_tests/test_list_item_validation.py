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
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        
        # Домашняя страница обновляется, и появляется сообщение об ошибке,
        # которое говорит, что элементы списка не должны быть пустыми
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        
        # Теперь Эрнест уже пробует по-нормальному что-то добавить
        # Должно сработать
        self.browser.find_element_by_id('id_new_item').send_keys('Scratch a turnip')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Scratch a turnip')
        
        # Каким бы странным это не казалось, он пытается
        # повторить трюк с пустым полем
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        
        # Результат такой же
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        
        # И он может исправить его, заполнив нейким текстом
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Scratch a turnip')
        self.wait_for_row_in_list_table('2: Make tea')
        
        self.fail('End test!')