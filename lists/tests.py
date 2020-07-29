from django.urls import resolve
from django.test import TestCase
from lists.views import home_page

class SmokeTest(TestCase):
    """тест на токсичность"""
    
    def test_bad_math(self):
        """Тест: неправильные математические расчёты"""
        
        self.assertEqual(1 + 1, 3)
        
class HomePageTest(TestCase):
    """Тест домашней страницы"""
    
    def test_root_url_resolves_to_home_page_view(self):
        """Тест: корневой url преобразуется в представление
        домашней страницы"""
        
        # resolve используется дл нахождения функции-обработчика в соответствии с url-адресом
        found = resolve('/')
        self.assertEqual(found.func, home_page)