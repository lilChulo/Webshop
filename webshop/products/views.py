# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Prüfen, ob der aktuelle Benutzer der Ersteller des Produkts oder ein Administrator ist
    if request.user == product.created_by or request.user.is_staff:
        # Wenn die Anfrage eine POST-Anfrage ist, das Produkt löschen
        if request.method == 'POST':
            product.delete()
            return redirect('product-list') 
        return render(request, 'products/product-delete.html', {'product': product})
    else:
        pass