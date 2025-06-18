from django.urls import path
from . import views

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
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
