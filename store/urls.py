from django.urls import path
from . import views
urlpatterns=[
    path('add_cart/',views.cart,name='cart'),
    path('add_cart/<str:product_id>/',views.add_cart,name='add_cart'),
   
    path('increment_iteam/<str:cart_product_id>/',views.increment,name='increment'),

    path('remove_cart/<str:product_id>/',views.remove_cart,name='remove_cart'),
    path('delete_cart/<str:cart_iteam_id>/',views.delete_cart,name='delete_cart'),
    path('single_product/<str:pk>/',views.single_product,name='single_product'),
    path('',views.home,name='home'),
    path('store/',views.store,name='store'),
    path('store/<str:cat_name>/',views.store_cat,name='store_cat'), 
    path('checkout/',views.checkout,name='checkout')
]