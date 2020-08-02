# django
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

# first-party
from lists.views import home_page
from lists.models import Item

        
class HomePageTest(TestCase):
    """Тест: домашняя страница"""

    def test_home_page_returns_correct_html(self):
        '''Тест: домашняя страница возращает правильный html'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
    def test_can_save_POST_request(self):
        '''Тест: можно сохранить POST-запрос'''
        self.client.post('/', data={'item_text': 'A new list item'})
        # сохраняется ли объект и его свойства через POST-запрос?
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
     
    def test_redirects_after_POST(self):
        """Тест: перенаправление после POST-запроса"""
        response = self.client.post('/', data={'item_text': 'A new list item'})   
        # вставить сюда pdb и посмотреть response изнутри
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
            
    def test_displays_all_list_items(self):
        """Тест: отображение всех элементов списка"""
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        
        response = self.client.get('/')
        
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


class ItemModelTest(TestCase):
    """Тест модели элемента списка задач"""
    
    def test_saving_and_retrieving_items(self):
        """Тест сохранения и получения элементов списка"""
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
    
    def test_only_saves_items_when_necessary(self):
        """Тест: элементы списка сохраняются только по надобности"""
        
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
        