# django
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

# first-party
from lists.views import home_page
from lists.models import Item, List

        
class HomePageTest(TestCase):
    """Тест: домашняя страница"""

    def test_home_page_returns_correct_html(self):
        '''Тест: домашняя страница возращает правильный html'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):
    """Тест модели элемента списка задач"""
    
    def test_saving_and_retrieving_items(self):
        """Тест сохранения и получения элементов списка""" 
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    """Тест представдения списка"""

    def test_uses_list_template(self):
        """Тест: используется шаблон списка"""
        response = self.client.get('/lists/one-of-a-kind-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
          
    def test_display_all_items(self):
        """Тест: отображаются все элементы списка"""
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        
        response = self.client.get('/lists/one-of-a-kind-list-in-the-world/')
        
        # assertContains (Django фича) умеет декодировать ответ и искать в нём текст самостоятельно
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        
        
class NewListTest(TestCase):
    """Тест нового списка"""
    
    def test_can_save_POST_request(self):
        """Тест: можно сохранить POST-запрос"""
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        # сохраняется ли объект и его свойства через POST-запрос?
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        
    def test_redirects_after_POST(self):
        """Тест: перенаправление после POST-запроса"""
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})   
        # вставить сюда pdb и посмотреть response изнутри
        self.assertRedirects(response, '/lists/one-of-a-kind-list-in-the-world/')