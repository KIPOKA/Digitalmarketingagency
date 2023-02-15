from math import ceil
from django.shortcuts import redirect, render
from digitalapp.models import Product
from django.urls import reverse
import uuid
from django.conf import settings
import stripe

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import OrderForm


# Create your views here.


def home(request):
    return render(request, 'index.html')


def purchase(request):
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
    #context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
    return render(request, 'purchase.html', params)


# Check out session

@csrf_exempt
def paid(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1MIBiPBDJFEKnZiZelNhtczE',
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/complete',
        cancel_url='http://127.0.0.1:8000/purchase',
        # success_url=request.build_absolute_uri(
        #    reverse('checkout')) + '?session_id={CHECKOUT_SESSION_ID}',
        # cancel_url=request.build_absolute_uri(reverse('payment')),

    )

    print(f"Session: {session}")

    context = {
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY

    }

    return JsonResponse({'sessionId': session.id})
    # return render(request, 'purchase', context)


def complete(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print("Done")
            form.save()
            return render(request, 'index.html', {'form': form})
    form = OrderForm()
    return render(request, 'form.html', {'form': form})
