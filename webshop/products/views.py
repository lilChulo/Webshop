# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, ProductImageFormSet, ReviewForm
from .models import ProductImage, Product, Review
from django.db.models import Q


@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')  # Get the list of uploaded files

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user
            product.save()

            for file in files:
                ProductImage.objects.create(product=product, images=file)

            return redirect('product:product-list')
        else:
            print(product_form.errors)
    else:
        product_form = ProductForm()

    return render(request, 'products/product-create.html', {
        'product_form': product_form,
    })


def list_all_products(request):
    products = Product.objects.all()
    return render(request, 'products/product-list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    user_review = None

    if request.user.is_authenticated:
        try:
            user_review = product.reviews.get(user=request.user)
        except Review.DoesNotExist:
            pass

    if request.method == 'POST' and request.user.is_authenticated:
        if user_review:
            form = ReviewForm(request.POST, instance=user_review)
        else:
            form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            
            # redirect after saving
            return redirect('product:product-detail', product_id=product.id)
    else:
        form = ReviewForm(instance=user_review) if user_review else ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    }
    return render(request, 'products/product-detail.html', context)


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user == product.created_by or request.user.is_staff:
        if request.method == 'POST':
            product.delete()
            return redirect('product:product-list')
        return render(request, 'products/product-delete.html', {'product': product})
    else:
        pass


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Update product details
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')

        # Handle existing PDF deletion
        if 'delete_pdf' in request.POST and request.POST['delete_pdf'] == 'yes':
            product.product_info_pdf.delete()
            product.product_info_pdf = None

        # Handle uploading a new PDF
        new_pdf = request.FILES.get('new_pdf')
        if new_pdf:
            # Delete existing PDF if there is one
            if product.product_info_pdf:
                product.product_info_pdf.delete()
            product.product_info_pdf = new_pdf

        # Save product changes
        product.save()

        # Handle deleting individual images
        if 'delete_file' in request.POST:
            file_id = request.POST.get('delete_file')
            image_to_delete = ProductImage.objects.get(id=file_id)
            image_to_delete.images.delete()
            image_to_delete.delete()

        # Handle uploading additional images
        additional_images = request.FILES.getlist('additional_images')
        for image in additional_images:
            ProductImage.objects.create(product=product, images=image)

        return redirect('product:product-detail', product_id=product.id)

    context = {
        'product': product,
    }
    return render(request, 'products/product-edit.html', context)


def search_products(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(other_field__icontains=query) |
            Q(rating__icontains=query)
        )
    else:
        results = Product.objects.none()
    return render(request, 'products/search-results.html', {'results': results, 'query': query})


@login_required
def delete_review(request, review_id):
    review = Review.objects.get(id=int(review_id))
    if request.user == review.user or request.user.is_superuser:
        review.delete()
        return redirect('product:product-detail', product_id=review.product.id)
    else:
        pass

    
@login_required
def vote_review(request, review_id, up_or_down):
    review = Review.objects.get(id=int(review_id))
    review.vote(request.user, up_or_down)
    return redirect('product:product-detail', product_id=review.product.id)