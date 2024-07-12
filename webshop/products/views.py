# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, ReviewForm
from .models import ProductImage, Product, Review
from django.db.models import Q, Avg


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
    reviews = Review.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

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

            # Redirect after saving
            return redirect('product:product-detail', product_id=product.id)
    else:
        form = ReviewForm(instance=user_review) if user_review else ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
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
        try:
            rating_filter = int(query)  # Versuchen, die Eingabe in eine Ganzzahl umzuwandeln
            results = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(other_field__icontains=query) |
                Q(rating=rating_filter)  # Genau nach Bewertung filtern
            )
        except ValueError:
            results = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(other_field__icontains=query)
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


def product_list(request):
    rating = request.GET.get('rating')
    if rating:
        products = Product.objects.annotate(average_rating=Avg('reviews__rating')).filter(average_rating=rating)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'rating': rating
    }
    return render(request, 'products/product-list.html', context)
