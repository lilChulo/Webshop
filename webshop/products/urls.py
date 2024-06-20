# products/urls.py
from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('add/', views.add_product, name='product-create'),
    path('', views.list_all_products, name='product-list'),
    path('<int:product_id>/', views.product_detail, name='product-detail'),
    path('<int:product_id>/delete/', views.delete_product, name='delete-product'),
    path('prod/<int:product_id>/edit/', views.edit_product, name='edit-product'),
    path('search/', views.search_products, name='search'),
]