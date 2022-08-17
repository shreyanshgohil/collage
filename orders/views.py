from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from store.models import CartItem
from .forms import Create_order
# Create your views here.
def place_order(request):
    cart_iteams = CartItem.objects.filter(user=request.user)
    total_itaem=cart_iteams.count()
    if total_itaem <=  0:
        return redirect('store')
 
    form = Create_order()
    if request.method == 'POST':
        form = Create_order(request.POST)
        if form.is_valid():
            form.first_name= form.cleaned_data['first_name']
            form.last_name= form.cleaned_data['last_name']
            form.email= form.cleaned_data['email']
            form.phone= form.cleaned_data['phone']
            form.address_line_1= form.cleaned_data['address_line_1']
            form.address_line_2= form.cleaned_data['address_line_2']
            form.city= form.cleaned_data['city']
            form.state= form.cleaned_data['state']
            form.country= form.cleaned_data['country']
            form.order_note= form.cleaned_data['first_name']
            form.save()
            return redirect('home')