from django.urls import path

from order import views

urlpatterns = [
    path('cart', views.CartView.as_view(), name='order-cart'),
]