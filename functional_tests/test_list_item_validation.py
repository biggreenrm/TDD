from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip


class ItemValidationTest(FunctionalTest):
    """Тест валидации элементов списка"""
    
    @skip
    def test_cannot_add_empty_list_items(self):
        """Тест: нелья добавлять пустые элементы списка"""