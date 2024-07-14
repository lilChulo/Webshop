from pyexpat.errors import messages

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, ReportedReview
from products.forms import ProductForm, Review


def is_customerservice(user):
    return user.groups.filter(name='CustomerService').exists() or user.is_superuser


@staff_member_required
@user_passes_test(is_customerservice)
def dashboard(request):
    products = Product.objects.all()
    return render(request, 'customerservice/dashboard.html', {'products': products})


@staff_member_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customerservice:dashboard')
    else:
        form = ProductForm()
    return render(request, 'customerservice/create_product.html', {'form': form})


@login_required
@user_passes_test(is_customerservice)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('customerservice:dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'customerservice/edit_product.html', {'form': form, 'product': product})


@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('customerservice:dashboard')
    return render(request, 'customerservice/delete_product.html', {'product': product})


@login_required
@user_passes_test(is_customerservice)
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('product:product-detail', product_id=review.product.id)
    return render(request, 'products/confirm_delete_review.html', {'review': review})


@permission_required('auth.view_users', raise_exception=True)
def customer_service_dashboard(request):
    products = Product.objects.all()
    reported_reviews = ReportedReview.objects.all()
    context = {
        'products': products,
        'reported_reviews': reported_reviews
    }
    return render(request, 'customerservice/dashboard.html', context)