from django.conf import settings
from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

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
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # Save order
        order = Orders(
            items_json=items_json,
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone
        )
        order.save()

        # Save order update
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        # Send confirmation email
        send_mail(
            'Order Confirmation',
            f'Thank you for your order, {name}! Your order ID is {order.order_id}.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Render thank you page with Stripe key
        context = {
            'thank': True,
            'id': order.order_id,
            'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY
        }
        return render(request, 'shop/checkout.html', context)

    # GET request
    return render(request, 'shop/checkout.html', {'stripe_pub_key': settings.STRIPE_PUBLISHABLE_KEY})


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

@csrf_exempt
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        try:
            YOUR_DOMAIN = "http://127.0.0.1:8000"
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Your MAC Order',
                            },
                            'unit_amount': int(float(request.POST.get('amount')) * 100),  # amount in cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/shop/success/',
                cancel_url=YOUR_DOMAIN + '/shop/cancel/',
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
def success(request):
    return render(request, 'shop/success.html')

def cancel(request):
    return render(request, 'shop/cancel.html')
