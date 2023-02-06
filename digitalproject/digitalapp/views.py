from math import ceil
from django.shortcuts import redirect, render
from digitalapp.models import Product, Orders, OrderUpdate
from django.urls import reverse, reverse_lazy
from django.contrib import messages
import uuid
from django.conf import settings
import stripe
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
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
        success_url='http://127.0.0.1:8000/payment',
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


class ProductCreateView(CreateView):
    model = Orders
    fields = '__all__'
    template_name = "digitalapp/payment.html"
    success_url = reverse_lazy("home")

# def checkout(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, "Login & Try Again")
#         return redirect('digitalauth/login')
#     if request.method == "POST":

#         company_name = request.POST['company_name']
#         amount = request.POST.get('price')
#         email = request.POST.get('email')
#         subject = request.POST['subject']
#         content = request.POST['content']
#         phone = request.POST['phone']

#         order = Orders.objects.create(company_name=company_name,
#                                       amount=amount, email=email, subject=subject, content=content, phone=phone)
#         order.save()

#         return render(request, 'base.html')

#     return render(request, 'base.html')


def payment(request):
    return render(request, 'payment.html')
