from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    """Тест для нового посетителя"""
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        """Подтверждение присутствия строки в таблице списка"""
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        """Тест: можно начать список и получить его позже"""
        
        # Эрнест где-то услыхал, что списки дел экономят психическую энергию
        # которой ему маловато в последнее время
        # Он решил оценить домашнюю страницу такого приложения
        self.browser.get('http://localhost:8000')

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
        time.sleep(3)
        
        self.check_for_row_in_list_table('1: Привести себя в порядок')
        # Текстовое поле по-прежнему приглашает Эрнеста сделать запись 
        # Что ж, пора "Убрать весь хлам на кухне"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Убрать весь хлам на кухне')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        
        # Страница снова обновляется и теперь показывает оба элемента списка
        self.check_for_row_in_list_table("1: Привести себя в порядок")
        self.check_for_row_in_list_table("2: Убрать весь хлам на кухне")
        # Эрнесту интересно, запомнит ли сайт еге список. Далее он видит, что 
        # сайт сгенерировал для неге уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.
        self.fail('Закончить тест!')
        # Эрнест посещает этот URL-адрес и обнаруживает там свой сохранённый список

        # Удовлетворённый своими "амбициозными планами", Эрнест снова засыпает

if __name__ == "__main__":
    unittest.main(warnings='ignore')
    