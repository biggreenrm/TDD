# django
from django.urls import resolve
from django.utils.html import escape
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

# first-party
from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


"""
Это - набор модульных тестов для представлений. И их тут много.
"""
        
class HomePageTest(TestCase):
    """Тест: домашняя страница"""

    def test_home_page_returns_correct_html(self):
        '''Тест: домашняя страница возращает правильный html'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_page_uses_item_form(self):
        """Тест: домашняя страница использует правильную форму"""
        response = self.client.get('/')
        # IsInstance проверяет соответствует ли проверяемый аргумент классу (второй аргумент)
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    """Тест представления списка"""

    def post_invalid_input(self):
        """Отправляет недопустимый ввод"""
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )
    
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
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        """Тест: сохранение в существующий список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text': 'A new list item to an existing list'})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item to an existing list')
        self.assertEqual(new_item.list, correct_list)
    
    def test_POST_redirects_to_list_view(self):
        """Тест: переадресуется в представление списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text': 'A new list item to an existing list'})
        
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
    
    def test_for_invalid_input_nothing_saved_to_db(self):
        """Тест: недопустимый ввод не сохраняется в БД"""
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
        
    def test_for_invalid_input_renders_list_template(self):
        """Тест: после недопустимого ввода отображается шаблон спсика"""
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
    
    def test_for_invalid_input_passes_form_to_template(self):
        """Тест: после недопустимого ввода форма передаётся в шаблон"""
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)
        
    def test_for_invalid_input_shows_error_on_page(self):
        """Тест: после недопустимого ввода отображается ошибка"""
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
        
    def test_displays_item_form(self):
        """Тест: отображение формы для элемента"""
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')
          
class NewListTest(TestCase):
    """Тест нового списка"""
    
    def test_can_save_POST_request(self):
        """Тест: можно сохранить POST-запрос"""
        self.client.post('/lists/new', data={'text': 'A new list item'})
        # сохраняется ли объект и его свойства через POST-запрос?
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        
    def test_redirects_after_POST(self):
        """Тест: перенаправление после POST-запроса"""
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')
    
    def test_for_invalid_input_renders_home_template(self):
        """Тест: недопустимый ввод отображает домашний шаблон"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        
    def test_validation_error_are_shown_on_home_page(self):
        """Тест: ошибки валидации выводятся на домашней странице"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
    
    def test_for_invalid_input_passes_form_to_template(self):
        """Тест: форма передаётся в шаблон после недопустимого ввода"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)
        
    def test_invalid_list_items_arent_saved(self):
        """Тест: сохраняются недопустимые элементы списка"""
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)