from django.db import models

class Item(models.Model):
    """Модель задачи из списка"""
    
    text = models.TextField(default='')
