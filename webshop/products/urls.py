# products/urls.py
from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('add/', views.add_product, name='product-create'),
    path('', views.product_list, name='product-list'),
    path('product/<int:product_id>/', views.product_detail, name='product-detail'),
    path('prod/<int:product_id>/delete/', views.delete_product, name='delete-product'),
    path('prod/<int:product_id>/edit/', views.edit_product, name='edit-product'),
    path('search/', views.search_products, name='search'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('prod/review/<int:review_id>/vote/<str:up_or_down>/', views.vote_review, name='vote-review'),
    path('prod/review/<int:review_id>/delete/', views.delete_review, name='delete-review'),
    path('prod/review/<int:review_id>/vote/<str:up_or_down>/', views.vote_review, name='vote-review'),
    path('product/<int:product_id>/review/<int:review_id>/report/', views.report_review, name='report-review'),
]
