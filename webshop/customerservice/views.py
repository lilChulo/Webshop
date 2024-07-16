from django.contrib import messages 
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, ReportedReview
from products.forms import ProductForm, Review


def is_customerservice(user):
    return user.groups.filter(name='CustomerService').exists() or user.is_superuser


@staff_member_required
@user_passes_test(is_customerservice)
def dashboard(request):
    products = Product.objects.all()
    reported_reviews = ReportedReview.objects.select_related('review').all()

    context = {
        'products': products,
        'reported_reviews': reported_reviews,
    }
    return render(request, 'customerservice/dashboard.html', context)


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

def delete_reported_review(request, reported_review_id):
    reported_review = get_object_or_404(ReportedReview, id=reported_review_id)
    
    if request.method == 'POST':
        reported_review.delete()
        return redirect('customerservice:dashboard')

    return redirect('customerservice:dashboard')  

@login_required
def toggle_resolve_reported_review(request, reported_review_id):
    reported_review = get_object_or_404(ReportedReview, id=reported_review_id)
    reported_review.resolved = not reported_review.resolved
    reported_review.save()
    if reported_review.resolved:
        messages.success(request, 'Review marked as resolved.')
    else:
        messages.success(request, 'Review marked as unresolved.')
    return redirect('customerservice:dashboard')

def delete_review_and_resolve(request, reported_review_id):
    reported_review = get_object_or_404(ReportedReview, pk=reported_review_id)

    # Speichern des review_id, bevor das ReportedReview Objekt gespeichert wird
    review_id = reported_review.review_id

    if request.method == 'POST':
        # Setzen des 'resolved' Flags auf True
        reported_review.resolved = True
        reported_review.save()

        # Löschung des zugehörigen Review Objekts
        review = get_object_or_404(Review, pk=review_id)
        product_id = review.product.id  # Produkt-ID des Reviews speichern, um später zur Produkt-Detailseite zu navigieren
        review.delete()

        # Erfolgsnachricht
        messages.success(request, f"The review with id '{review_id}' has been deleted and the report resolved.")

    # Weiterleitung zur Produkt-Detailseite, auf der das Review geschrieben wurde
    return redirect('product:product-detail', product_id=product_id)
