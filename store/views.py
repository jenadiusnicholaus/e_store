import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
from django.utils.datetime_safe import datetime
from django.views.generic import DetailView
from django.views.generic.base import View
from .models import *
from .forms import CheckoutForm


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


# The views created here are used to render the html files created
# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products, }
    return render(request, 'store/store.html', context)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Product_details(DetailView):
    model = Product
    template_name = 'store/product_details.html'


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    order_qs = Order.objects.filter(customer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(product__pk=product.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'this item quantity was updated ')
        else:
            messages.info(request, 'this item was added to your cart ')

            order.order_items.add(order_item)
            return redirect('/', )
    else:

        order = Order.objects.create(customer=request.user, ref_id=create_ref_code())

        order.order_items.add(order_item)
        messages.info(request, 'this item was added to your cart ')
    return redirect('/')


class CartIterms(LoginRequiredMixin, View):
    def get(self, orgs, *args, **kwargs):

        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            context = {
                'cart_items': order
            }
            return render(self.request, 'store/cart.html', context=context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have thr active order')
            return redirect('/')


@login_required
def remove_from_cart(request, pk):
    # let get an item from thr item list
    product = get_object_or_404(Product, pk=pk)
    # let check if the user has the oder in that is not ordered yet
    order_qs = Order.objects.filter(customer=request.user, ordered=-False)
    # if that the user has the order in the order list
    if order_qs.exists():
        # then grab the that order
        order = order_qs[0]
        # and check the specific oder item regarding to slug item in the request
        if order.order_items.filter(product__pk=product.pk).exists():
            """
             after that now we need to grab that oder from the oder_item by filtering using
             user in request and ordered not, and the item itself
            """
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            """
            then finally we remove that oder from cart completely
            """
            order.order_items.remove(order_item)
            messages.info(request, 'this item was removed from your cart ')
        else:
            # a message to the user that there is no that kind of query set
            messages.info(request, 'this item was was not in your cart ')
            return redirect('/', )
    else:
        messages.info(request, "You don't have an active order")
        return redirect('/')
    return redirect('/')


class CheckOut(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)
        form = CheckoutForm()
        context = {
            'order': order,
            'form': form
        }
        return render(self.request, 'store/checkout.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)
        form = CheckoutForm(self.request.POST)
        if form.is_valid():
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zipcode = form.cleaned_data.get('zipcode')
            # # added field
            description = form.cleaned_data.get('description')
            shipping_address = ShippingAddress()
            shipping_address.customer = self.request.user
            shipping_address.state = state
            shipping_address.address = address
            shipping_address.city = city
            shipping_address.zipcode = zipcode
            shipping_address.description = description
            shipping_address.save()

            order.shippingAddress = shipping_address
            order.save()

            # redirect to payment option
            payment_option = self.request.POST.get('option')

            if payment_option == 'paypal':
                print(payment_option)
                messages.success(self.request, ' Chosen paypal')
                return redirect('payment', payment_option=payment_option)
            elif payment_option:
                print(payment_option)
                messages.success(self.request, ' Chosen skrill')
                return redirect('payment', payment_option=payment_option)
        else:
            messages.success(self.request, 'form is not ok')
            return redirect('checkout')


class Payment(View):
    def get(self, request, payment_option, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)
        context = {
            'order': order
        }
        if payment_option == 'skrill':
            return render(request, template_name='store/skrill.html' , context=context)
        elif payment_option == 'paypal':
            return render(request, template_name='store/skrill.html',context=context)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#
def cart(request):
    # checking if the user is authenticated
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []  # when a user isn't authenticated

        order = {'get_cart-total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []  # when a user isn't authenticated
        order = {'get_cart-total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    # context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', )


# Added registered page
def register(request):
    context = {}
    return render(request, 'store/register.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
