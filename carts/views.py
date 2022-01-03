from django.shortcuts import redirect, render
from store.models import Product
from .models import Cart,CartItem

def _cart_id(request):
    cart =  request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

#add to cart function
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try: 
        cart =  Cart.objects.get(cart_id=_cart_id(request))#get  the cart using cart_id in session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1 #cart_tem increment by one
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product =  product,
            quantity =  1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')


# Create your views here.
def cart(request):
    return render (request, 'store/cart.html')