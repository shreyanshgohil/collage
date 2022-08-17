from django.db import models
from django.contrib.auth.models import User
import uuid

from store.models import Color, Product, Size


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return str(self.payment_id)

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled')
        )

    user = models.ForeignKey(User,on_delete=models.CharField)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name =  models.CharField(max_length=100,null=True,blank=True)
    phone =  models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address_line_1 = models.CharField(max_length=50,blank=True,null=True)
    address_line_2 = models.CharField(max_length=50,blank=True,null=True)
    county =models.CharField(max_length=50,blank=True,null=True)
    state =models.CharField(max_length=50,blank=True,null=True)
    city =models.CharField(max_length=50,blank=True,null=True)
    order_note =models.CharField(max_length=50,blank=True,null=True)
    order_total =models.FloatField()
    status = models.CharField(max_length=100,choices=STATUS,default='New')
    ip =models.CharField(max_length=50,blank=True,null=True)
    is_orderd = models.BooleanField(default=False)
    updated_at  =models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.user.first_name

class OrderProduct(models.Model):
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.ManyToManyField(Size)
    color = models.ManyToManyField(Color)
    quantity = models.ImageField()
    product_price = models.FloatField()
    orderd = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)