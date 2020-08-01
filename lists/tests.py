# django
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

# first-party
from lists.views import home_page

        
class HomePageTest(TestCase):
    """Тест: домашняя страница"""

    def test_home_page_returns_correct_html(self):
        '''Тест: домашняя страница возращает правильный html'''
        
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
    def test_can_save_POST_request(self):
        '''Тест: можно сохранить POST-запрос'''
        # item_text - это данные формы на home page '/'
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')