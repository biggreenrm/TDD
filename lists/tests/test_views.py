# django
from django.urls import resolve
from django.utils.html import escape
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


class ListViewTest(TestCase):
    """Тест представдения списка"""

    def test_uses_list_template(self):
        """Тест: используется шаблон списка"""
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')
          
    def test_display_only_items_for_that_list(self):
        """Тест: отображаются элементы для конкретного списка"""
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='another element 1', list=other_list)
        Item.objects.create(text='another element 2', list=other_list)
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        # assertContains (Django фича) умеет декодировать ответ и искать в нём текст самостоятельно
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'another element 1')
        self.assertNotContains(response, 'another element 2')
    
    def test_passes_correct_list_to_template(self):
        """Тест: передаётся правильный шаблон списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        self.assertEqual(response.context['list'], correct_list)
        
        
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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        """Тест: сохранение в существующий список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new list item to an existing list'})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item to an existing list')
        self.assertEqual(new_item.list, correct_list)
    
    def test_redirects_to_list_view(self):
        """Тест: переадресуется в представление списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new list item to an existing list'})
        
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
    
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        """Тест: сообщения об ошибке возвращаются на домашнюю страницу"""
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
        
    def test_invalid_list_items_arent_saved(self):
        """Тест: сохраняются недопустимые элементы списка"""
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)