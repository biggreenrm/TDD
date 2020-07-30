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
        time.sleep(1)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == "1: Привести себя в порядок" for row in rows),
            'Новый элемент списка не появился в таблице'
        )
        # Текстовое поле по-прежнему приглашает Эрнеста сделать запись 
        # Что ж, пора "Убрать весь хлам на кухне"
        self.fail('Закончить тест!')
        # Страница снова обновляется и теперь показывает оба элемента списка

        # Эрнесту интересно, запомнит ли сайт еге список. Далее он видит, что 
        # сайт сгенерировал для неге уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.

        # Эрнест посещает этот URL-адрес и обнаруживает там свой сохранённый список

        # Удовлетворённый своими "амбициозными планами", Эрнест снова засыпает

if __name__ == "__main__":
    unittest.main(warnings='ignore')
    