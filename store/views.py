from django.shortcuts import render
from django.views.generic.base import View

from .models import *




# The views created here are used to render the html files created
# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    # checking if the user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []  # when a user isn't authenticated
        order = {'get_cart-total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)


# Added registered page
def register(request):
    context = {}
    return render(request, 'store/register.html', context)
