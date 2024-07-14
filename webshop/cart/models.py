from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from products.models import Product


from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


# def add_item_to_shopping_cart(myuser, product):
#     """
#     Creates a shopping cart item and
#     assigns it to the shopping cart
#     of the current user.
#     """

#     try:
#         shopping_cart = ShoppingCart.objects.get(myuser=myuser)
#     except ObjectDoesNotExist:
#         shopping_cart = ShoppingCart.objects.create(myuser=myuser)

#     product_id = product.id
#     product_name = product.name
#     price = product.price

#     ShoppingCartItem.objects.create(
#         product_id=product_id,
#         product_name=product.name,
#         price=price,
#         quantity=1,  # the quantity is hard coded here, for simplicity reasons
#         shopping_cart=shopping_cart
#     )
    
class ShoppingCart(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    myuser = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_number_of_items(self):
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        num_shopping_cart_items = len(shopping_cart_items)

        return num_shopping_cart_items

    def get_total(self):
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        total = sum([
            item.price * item.quantity
            for item
            in shopping_cart_items
        ])
        return total
    
    def clear_items(self):
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        shopping_cart_items.delete()
        
    def total_items(self):
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        total_items = sum([item.quantity for item in shopping_cart_items])
        return total_items
    

class ShoppingCartItem(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.IntegerField(default=1)
    shopping_cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE
    )
    
    def subtotal(self):
        return self.price * self.quantity