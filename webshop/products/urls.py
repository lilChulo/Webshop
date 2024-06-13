# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_product, name='product-create'),
    path('list/', views.list_all_products, name='product-list'),
    path('<int:product_id>/', views.product_detail, name='product-detail'),
    path('<int:product_id>/delete/', views.delete_product, name='delete-product'),
]