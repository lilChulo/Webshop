from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('show', views.show_shopping_cart, name='shopping-cart-show'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear/', views.clear_cart, name='clear-cart'),
]
