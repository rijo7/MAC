import paypalrestsdk
from django.conf import settings
from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
from django.http import JsonResponse
import json

# Create your views here.
from django.http import HttpResponse


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = ceil(n / 4)

        # Break the product list into chunks of 4
        prod_chunks = [prod[i:i+4] for i in range(0, n, 4)]

        # Append category, product chunks, range object, and nSlides
        allProds.append([cat, prod_chunks, range(nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank=False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request, 'shop/contact.html', {'thank':thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if order.exists():
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = [{'text': item.update_desc, 'time': item.timestamp} for item in update]
                response = [updates, json.loads(order[0].items_json)]
            else:
                response = [[], {}]  # Provide empty data in case of no match
            return JsonResponse(response, safe=False)  # Use JsonResponse for proper JSON response
        except Exception as e:
            return JsonResponse([[], {}], safe=False)  # Return empty data on exception

    return render(request, 'shop/tracker.html')


def search(request):
    query = request.GET.get('query')
    print("Search query:", query)  # Debugging

    if query:
        results = Product.objects.filter(product_name__icontains=query)
        print("Search results:", results)  # Debugging
    else:
        results = Product.objects.all()  # or handle empty case differently
        print("No search query provided.")  # Debugging

    return render(request, 'shop/search_results.html', {'products': results, 'query': query})


def productView(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if product:
        return render(request, 'shop/prodView.html', {'product': product})
    else:
        # Handle the case where the product doesn't exist
        return HttpResponse("Product not found", status=404)



def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')


def quickview(request, product_id):
    product = Product.objects.get(id=product_id)
    product_data = {
        "name": product.product_name,
        "description": product.desc,
        "price": product.price,
        "images": [{"url": product.image.url}],
        "category": product.category,
        "subcategory": product.subcategory,
    }
    return JsonResponse(product_data)

def my_view(request):
    products = Product.objects.all()  # Example query
    return render(request, 'index.html', {'prod_list': products})

def quality_products(request):
    return render(request, 'shop/quality_products.html')

def fast_delivery(request):
    return render(request, 'shop/fast_delivery.html')

def customer_support(request):
    return render(request, 'shop/customer_support.html')

def learnmore(request):
    return render(request, 'shop/learnmore.html')


paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def create_payment(request):
    if request.method == 'POST':
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute/",
                "cancel_url": "http://localhost:8000/payment/cancel/"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Test Product",
                        "sku": "001",
                        "price": "10.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "10.00",
                    "currency": "USD"
                },
                "description": "This is a test payment."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return JsonResponse({'approval_url': approval_url})
        else:
            return JsonResponse({'error': payment.error})

    return render(request, 'shop/payment.html')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'shop/payment_success.html')
    else:
        return render(request, 'shop/payment_cancel.html')

def payment_success(request):
    return render(request, 'shop/payment_success.html')

def payment_cancel(request):
    return render(request, 'shop/payment_cancel.html')
