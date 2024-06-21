from django.shortcuts import render
from products.models import Product


def home(request):
    latest_products = Product.objects.order_by('-id')[:4]

    context = {
        'latest_products': latest_products,
        'user': request.user,
    }
    return render(request, 'home.html', context)
