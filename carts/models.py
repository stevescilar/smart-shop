from django.db import models
from carts.views import cart
from store.models import Product



#creating a function for the add to cart
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add = True)

    #overide object name
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product