from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product
from .models import Cart, CartItem


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get('cart_id')

    if not cart_id:
        cart = Cart.objects.create(user=request.user)
        request.session['cart_id'] = cart.id
    else:
        cart = Cart.objects.get(id=cart_id, user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1, 'item_price': product.price})

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1, 'item_price': product.price})
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart.update_totals()
    return redirect('cart:cart')


@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price if cart else 0
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart_item.delete()
    cart_item.cart.update_totals()
    return redirect('cart:cart')


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price if cart else 0
    return render(request, 'cart/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout_process(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.items.all().delete()
        cart.update_totals()
    return redirect('cart:cart')


def clear_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        CartItem.objects.filter(cart_id=cart_id).delete()
        del request.session['cart_id']
