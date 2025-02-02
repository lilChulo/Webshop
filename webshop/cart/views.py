from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product
from .models import ShoppingCart, ShoppingCartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.contrib import messages

@login_required
def show_shopping_cart(request):
    def create_context_object(
            shopping_cart_is_empty=True,
            shopping_cart_items=None,
            total=0.0
    ):
        return {
            'shopping_cart_is_empty': shopping_cart_is_empty,
            'shopping_cart_items': shopping_cart_items,
            'total': Decimal(total)  # The model expects a Decimal, not float!
        }

    myuser = request.user
    context = {}

    if myuser.is_authenticated:
        try:
            shopping_cart = ShoppingCart.objects.get(myuser=myuser)
            shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)
            total = shopping_cart.get_total()

            context = create_context_object(
                shopping_cart_is_empty=False,
                shopping_cart_items=shopping_cart_items,
                total=total
            )
        except ObjectDoesNotExist:  # User has no shopping cart
            # If no shopping cart exists, create an empty context
            context = create_context_object()
    else:
        # If user is not authenticated, create an empty context
        context = create_context_object()

    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        myuser = request.user

        quantity = int(request.POST.get('quantity', 1))

        try:
            shopping_cart = ShoppingCart.objects.get(myuser=myuser)
        except ShoppingCart.DoesNotExist:
            shopping_cart = ShoppingCart.objects.create(myuser=myuser)

        try:
            shopping_cart_item = ShoppingCartItem.objects.get(
                shopping_cart=shopping_cart,
                product_id=product.id
            )
            shopping_cart_item.quantity += quantity
            shopping_cart_item.save()
        except ShoppingCartItem.DoesNotExist:
            ShoppingCartItem.objects.create(
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=quantity,
                shopping_cart=shopping_cart
            )

        return redirect('cart:shopping-cart-show')
    else:
        messages.warning(request, 'Please login to add items to your cart.')
        return redirect('login')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, pk=item_id)
    shopping_cart = cart_item.shopping_cart

    if request.method == 'POST':
        quantity = request.POST.get('quantity')

        try:
            quantity = int(quantity)
        except ValueError:
            return HttpResponseBadRequest("Invalid quantity")

        if quantity >= cart_item.quantity:
            # Remove the item completely if quantity to remove is greater or equal to the item's quantity
            cart_item.delete()
        else:
            # Reduce the quantity of the item
            cart_item.quantity -= quantity
            cart_item.save()

        # Update the total price in the shopping cart
        total = shopping_cart.get_total()
        shopping_cart.total = total
        shopping_cart.save()

    return redirect('cart:shopping-cart-show')


@login_required
def clear_cart(request):
    try:
        shopping_cart = ShoppingCart.objects.get(myuser=request.user)
    except ShoppingCart.DoesNotExist:
        shopping_cart = None
    
    if shopping_cart:
        shopping_cart.clear_items()
    
    return redirect('cart:shopping-cart-show')
