from django.urls import path
from . import views

app_name = 'customerservice'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
#     path('create/', views.create_product, name='create_product'),
#     path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
#     path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete-reported-review/<int:reported_review_id>/', views.delete_reported_review, name='delete-reported-review'),
    path('reported-review/<int:reported_review_id>/toggle-resolve/', views.toggle_resolve_reported_review, name='toggle-resolve-reported-review'),
    path('reported-review/<int:reported_review_id>/delete-review-and-resolve/', views.delete_review_and_resolve, name='delete-review-and-resolve'),
]
