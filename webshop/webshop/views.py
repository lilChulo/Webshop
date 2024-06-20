from django.shortcuts import render
from products.models import Product


def home(request):
    # Query the latest 4 products
    # This line of code is querying the database for the latest 4 products from the `Product` model.
    latest_products = Product.objects.order_by('-id')[:4]  # Beispiel: Sortiere nach ID absteigend, nimm die ersten 4

    context = {
        'latest_products': latest_products,
        'user': request.user,  # Übergebe den aktuellen Benutzer
    }
    return render(request, 'home.html', context)
