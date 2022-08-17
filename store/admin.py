from django.contrib import admin
from .models import Category,Product,Cart,CartItem,Color,Size
# Register your models here.

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable =('is_active',)
   
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Color)
admin.site.register(Size)
