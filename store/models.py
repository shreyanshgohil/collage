from django.urls import reverse
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    category_desc = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4,unique = True,primary_key = True,editable = False)

    def cat_url(self):
        return reverse('store_cat',args=[self.category_name])

    def __str__(self):
        return self.category_name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_desc = models.TextField()
    price_main = models.IntegerField(validators=[MinValueValidator(0)],blank=True,null=True)
    price_discount = models.IntegerField(validators=[MinValueValidator(0)])
    product_img = models.ImageField(default='default/default.jpg',null=True,blank =True,upload_to ='products' )
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    modified_date = models.DateTimeField(auto_now=True)
    colors = models.ManyToManyField('Color')
    sizes = models.ManyToManyField('Size')
    created = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default = uuid.uuid4,unique = True,primary_key = True,editable = False)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default = uuid.uuid4,unique = True,primary_key = True,editable = False)
    
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user  = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size_var = models.ManyToManyField('Size',blank=True) 
    color_var = models.ManyToManyField('Color',blank=True) 
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default = uuid.uuid4,unique = True,primary_key = True,editable = False)

    def sub_total(self):
        return self.product.price_discount * self.quantity

    def __str__(self):
        return str(self.product)

class Size(models.Model):
    size = models.CharField(max_length=150,unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default = uuid.uuid4,unique = True,primary_key = True,editable = False)

    def __str__(self):
        return self.size

class Color(models.Model):
    color = models.CharField(max_length=255,unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default = uuid.uuid4,unique = True,primary_key = True,editable = False)

    def __str__(self):
        return self.color

