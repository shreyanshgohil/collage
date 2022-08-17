from .models import Cart, CartItem, Category, Product
from .views import _cart_id,store


def menu_links(requst):
    links = Category.objects.all()
    return dict(links=links)


def counter(request):
    cart_count = 0
    cart = Cart.objects.filter(cart_id=_cart_id(request))
    if request.user.is_authenticated:
        cart_iteams = CartItem.objects.all().filter(user = request.user)
    else:
        cart_iteams = CartItem.objects.all().filter(cart=cart[:1])
    for cart_iteam in cart_iteams:
        cart_count += cart_iteam.quantity
    return dict(cart_count=cart_count)

