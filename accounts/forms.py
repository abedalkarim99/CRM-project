from django.forms import ModelForm
from .models import *


class Order_form(ModelForm) :
    class Meta :
        model = Order
        fields = '__all__' #['customer','','']