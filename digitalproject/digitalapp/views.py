from math import ceil
from django.shortcuts import redirect, render
from digitalapp.models import Product
from django.contrib import messages
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
    return render(request, 'purchase.html', params)


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('digitalauth/login')
    if request.method == "POST":

        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        Order = Orders(items_json=items_json, name=name, amount=amount, email=email, address1=address1,
                       address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,
                             update_desc="the order has been placed")
        update.save()
        thank = True
        id = Order.order_id
        oid = str(id)
        oid = str(id)
        param_dict = {

            'MID': 'add ur merchant id',
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')
