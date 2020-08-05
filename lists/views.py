# django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item


def home_page(request):
    """Домашняя страница"""
    return render(request, 'home.html')

def view_list(request):
    """Представление списка"""
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    """Представление нового списка"""
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text)
    return redirect('/lists/one-of-a-kind-list-in-the-world/')