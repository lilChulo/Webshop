# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product

def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user  # Set the created_by field
            product.save()
            return redirect('product-list')  # Replace 'product-list' with your actual URL name
    else:
        product_form = ProductForm()
    
    return render(request, 'products/product-create.html', {
        'product_form': product_form
    })
    
def list_all_products(request):
    products = Product.objects.all()
    return render(request, 'products/product-list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id) #return an object, or raise an Http404 exception
    return render(request, 'products/product-detail.html', {'product': product})