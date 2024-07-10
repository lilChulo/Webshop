from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_items = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def update_totals(self):
        cart_items = self.items.all()
        total_items = sum(item.quantity for item in cart_items)
        total_price = sum(item.subtotal() for item in cart_items)
        self.total_items = total_items
        self.total_price = total_price
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def subtotal(self):
        return self.quantity * self.item_price
