from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List


"""
Это - набор модульных тестов для моделей. Они проверяют отсутствие возможности сохранить пустых дел,
возможность сохранять дела в списки, получение абсолютного адреса списков.
"""


class ListModelTest(TestCase):
    """Тесты для модели списка задач"""

    def test_get_absolute_url(self):
        """Тест: абсолютный url доступен и его можно получить"""
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')


class ItemModelTest(TestCase):
    """Тесты для модели задачи в списке задач"""

    def test_default_text(self):
        """Тест: заданного по-умолчанию текста""" 
        item = Item()
        self.assertEqual(item.text, '')
    
    def test_cannot_save_empty_list_items(self):
        """Тест: нельзя добавлять пустые задачи в список"""
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        # не совсем понимаю как это работает, нужно разбираться
        with self.assertRaises(ValidationError):
            item.save()
            # ручной метод валидации (принудительный?)
            item.full_clean()
    
    def test_item_is_related_to_list(self):
        """Тест: задача связана со списком"""
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())
    
    def test_duplicate_items_are_invalid(self):
        """Тест: добавление одинаковых элементов в список недопустимо"""
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        """Тест: можно сохранять одинаковые элементы в разные списки"""
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean() # не должен поднять исключение
        
    def test_list_ordering(self):
        """Тест: таски выводятся в том же порядке, что и добавляются"""
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        """Тест: вывод в консоль объекта задачи представляет из себя строку"""
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')