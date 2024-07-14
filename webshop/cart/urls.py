from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
        path('cart/show', views.show_shopping_cart, name='shopping-cart-show'),
        path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
        path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
        path('cart/clear/', views.clear_cart, name='clear-cart'),
#     path('', views.cart_detail, name='cart'),
#     path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
#     path('checkout/', views.checkout, name='checkout'),
#     path('checkout-process/', views.checkout_process, name='checkout_process'),
]
