from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
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

#remove product from cart

def remove_cart (request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

#remove cart item completely

def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

#add items to cart
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        #calculations for items added to the cart
        for cart_item in cart_items: 
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (16 * total )/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    #create a context list to pass the items to cart template
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
        }
    return render (request, 'store/cart.html', context)