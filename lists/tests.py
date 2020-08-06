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