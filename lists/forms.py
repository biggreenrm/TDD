from django import forms
from .models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"

class ItemForm(forms.models.ModelForm):
    """Форма для элементов списка"""
    
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.widgets.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
    
    def save(self, for_list):
        # .instance даёт доступ к объекту, которому принадлежит форма
        self.instance.list = for_list
        return super().save()