from math import ceil
from django.shortcuts import render
from digitalapp.models import Product
# Create your views here.


def home(request):
    current_user = request.user
    print(current_user)
    allProducts = []
    catproducts = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catproducts}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProducts.append([prod, range(1, nSlides), nSlides])
    params = {'allProducts': allProducts}
    return render(request, 'index.html', params)
