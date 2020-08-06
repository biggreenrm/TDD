# django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List


def home_page(request):
    """Домашняя страница"""
    return render(request, 'home.html')

def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    """Представление нового списка"""
    list_ = List.objects.create()
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text, list=list_)
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    """Представление добавления в конкретный список"""
    list_ = List.objects.get(id=list_id)
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect (f'/lists/{list_.id}/')