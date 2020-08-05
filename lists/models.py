from django.db import models


class List(models.Model):
    """Модель списка задач"""
    pass


class Item(models.Model):
    """Модель задачи из списка"""
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)