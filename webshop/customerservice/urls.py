from django.urls import path
from . import views
from .views import customer_service_dashboard

app_name = 'customerservice'

urlpatterns = [
    path('dashboard/', customer_service_dashboard, name='customer_service_dashboard'),
    path('create/', views.create_product, name='create_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
