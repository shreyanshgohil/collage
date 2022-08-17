from .models import Order
from django.forms.models import ModelForm

class Create_order(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','phone','email','address_line_1','address_line_2','county','state','city','order_note']
    
    