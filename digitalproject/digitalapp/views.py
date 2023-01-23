from math import ceil
from django.shortcuts import redirect, render
from digitalapp.models import Product
from django.urls import reverse
from django.contrib import messages
import uuid
from django.conf import settings
import stripe
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
        success_url='http://127.0.0.1:8000/purchase',
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

# def checkout(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, "Login & Try Again")
#         return redirect('digitalauth/login')
#     if request.method == "POST":

#         items_json = request.POST.get('itemsJson', '')
#         name = request.POST.get('name', '')
#         amount = request.POST.get('amt')
#         email = request.POST.get('email', '')
#         address1 = request.POST.get('address1', '')
#         address2 = request.POST.get('address2', '')
#         city = request.POST.get('city', '')
#         state = request.POST.get('state', '')
#         zip_code = request.POST.get('zip_code', '')
#         phone = request.POST.get('phone', '')

#         Order = Orders(items_json=items_json, name=name, amount=amount, email=email, address1=address1,
#                        address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
#         print(amount)
#         Order.save()
#         update = OrderUpdate(order_id=Order.order_id,
#                              update_desc="the order has been placed")
#         update.save()
#         thank = True
#         id = Order.order_id
#         oid = str(id)
#         oid = str(id)
#         param_dict = {

#             'MID': 'add ur merchant id',
#             'ORDER_ID': oid,
#             'TXN_AMOUNT': str(amount),
#             'CUST_ID': email,
#             'INDUSTRY_TYPE_ID': 'Retail',
#             'WEBSITE': 'WEBSTAGING',
#             'CHANNEL_ID': 'WEB',
#             'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

#         }
#         param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
#             param_dict, MERCHANT_KEY)
#         return render(request, 'paytm.html', {'param_dict': param_dict})

#     return render(request, 'checkout.html')
