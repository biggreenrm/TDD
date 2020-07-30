# django
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

# first-party
from lists.views import home_page

        
class HomePageTest(TestCase):
    """Тест домашней страницы"""
    
    def test_root_url_resolves_to_home_page_view(self):
        """Тест: корневой url преобразуется в представление
        домашней страницы"""
        
        # resolve используется дл нахождения функции-обработчика в соответствии с url-адресом
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    
    def test_home_page_returns_correct_html(self):
        """Тест: домашняя страница возращает правильный html"""
        
        request = HttpRequest()
        response = home_page(request)
        # байт-код response'a (единицы и нули) декодируется в html через utf8
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.endswith('</html>'))