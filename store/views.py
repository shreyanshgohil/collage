from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models import Cart, Category, Product, CartItem, Size, Color
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    products = Product.objects.filter(is_available=True)
    context = {'products': products}
    return render(request, 'store/home.html', context)


def store_cat(request, cat_name):
    products = Product.objects.filter(category__category_name=cat_name)
    total_product = products.count()
    page = request.GET.get('page')
    results = 3
    paginator = Paginator(products, results)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)
    context = {'products': products,
               'total_product': total_product, 'paginator': paginator}
    return render(request, 'store/store.html', context)


def store(request):

    # for search
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    products = Product.objects.filter(Q(product_name__icontains=search_query) | Q(category__category_name__icontains=search_query))
    total_product = products.count()
    # end search

    # for Paginator
    page = request.GET.get('page')
    result = 3
    paginator = Paginator(products, result)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)

    # end paginator

    context = {'products': products, 'total_product': total_product,
               'paginator': paginator, 'search_query': search_query}
    return render(request, 'store/store.html', context,)

# for single product only


def single_product(request, pk):

    single_product = Product.objects.get(id=pk)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    context = {'product': single_product, 'in_cart': in_cart}
    return render(request, 'store/single-product.html', context)

# for cart


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):

    # variations
    product = Product.objects.get(id=product_id)  # geting the product
    color_web = request.GET.get('color')
    size_web = request.GET.get('size')

    # print('color',color_web)
    # print('size',size_web)
    color = Color.objects.get(color=color_web)
    size = Size.objects.get(size=size_web)
    # end variations

    # get the cart using cart id using session
    try:
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart.save()
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    if request.user.is_authenticated:
        cart_item_exists = CartItem.objects.filter(
            product=product, user=request.user, size_var=size, color_var=color).exists()
    else:
        cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart, size_var=size, color_var=color).exists()
    # print(cart_item_exists)

    if request.user.is_authenticated:
        if cart_item_exists:
            cart_item = CartItem.objects.get(product=product, user=request.user, cart=cart, size_var=size, color_var=color)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(user=request.user, product=product, cart=cart, quantity=1)
            cart_item.size_var.add(size)
            cart_item.color_var.add(color)
            cart_item.save()
    else:
        if cart_item_exists:
            cart_item = CartItem.objects.get(product=product, cart=cart, size_var=size, color_var=color)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
            cart_item.size_var.add(size)
            cart_item.color_var.add(color)
            cart_item.save()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_iteams=None):
    tax = 0
    grand_total = 0

    try:

        if request.user.is_authenticated:
            cart_iteams = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_iteams = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_iteam in cart_iteams:
            total += (cart_iteam.product.price_discount * cart_iteam.quantity)
            quantity += cart_iteam.quantity
        tax = (18 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {'total': total, 'quantity': quantity,
               'cart_iteams': cart_iteams, 'tax': tax, 'grand_total': grand_total}
    return render(request, 'store/cart.html', context)


def remove_cart(request, product_id):
    if request.user.is_authenticated:
        cart_iteam = CartItem.objects.get(id=product_id, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_iteam = CartItem.objects.get(id=product_id, cart=cart)
    if cart_iteam.quantity > 1:
        cart_iteam.quantity -= 1
        cart_iteam.save()
    else:
        cart_iteam.delete()

    return redirect('cart')


def delete_cart(request, cart_iteam_id):
    if request.user.is_authenticated:
        cart_iteam = CartItem.objects.get(user=request.user, id=cart_iteam_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_iteam = CartItem.objects.get(cart=cart, id=cart_iteam_id)
    cart_iteam.delete()
    return redirect('cart')


def increment(request, cart_product_id):
    if request.user.is_authenticated:
        cart_iteam = CartItem.objects.get(
            user=request.user, id=cart_product_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_iteam = CartItem.objects.get(cart=cart, id=cart_product_id)
    cart_iteam.quantity += 1
    cart_iteam.save()
    print(cart_iteam)
    return redirect('cart')


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_iteams=None):
    tax = 0
    grand_total = 0
    try:

        cart_iteams = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_iteam in cart_iteams:
            total += (cart_iteam.product.price_discount * cart_iteam.quantity)
            quantity += cart_iteam.quantity
        tax = (18 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {'total': total, 'quantity': quantity,
               'cart_iteams': cart_iteams, 'tax': tax, 'grand_total': grand_total}
    return render(request, 'store/checkout.html', context)
