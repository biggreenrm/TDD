from django.db import models
from django.core.urlresolvers import reverse

class List(models.Model):
    """Модель списка задач"""
    
    def get_absolute_url(self):
        """Получить абсолютный url"""
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    """Модель задачи из списка"""
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)