from django.urls import path
from . import views
from .views import create_payment, execute_payment, payment_success, payment_cancel

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path('quickview/<int:product_id>/', views.quickview, name='quickview'),
    path('quality-products/', views.quality_products, name='QualityProducts'),
    path('fast-delivery/', views.fast_delivery, name='FastDelivery'),
    path('customer-support/', views.customer_support, name='CustomerSupport'),
    path('learn-more/', views.learnmore, name='LearnMore'),
    path('search/', views.search, name='search'),
    path('payment/', views.create_payment, name='create-payment'),
    path('payment/execute/', views.execute_payment, name='execute-payment'),
    path('payment/success/', views.payment_success, name='payment-success'),
    path('payment/cancel/', views.payment_cancel, name='payment-cancel'),
]
