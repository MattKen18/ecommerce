from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
# Create your views here.

def store(response):
    template = 'store/store.html'
    products = Product.objects.all()
    context = {"products": products}

    return render(response, template, context)

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    order_item, created = OrderItem.objects.get_or_create(cart=cart, product=product)
    order_item.quantity += 1
    order_item.save()

    return redirect('store')

def cart(request):
    template = 'store/cart.html'
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = OrderItem.objects.filter(cart=cart)

    total_items = cart_items.count()

    total_price = 0
    for item in cart_items:
        total_price += item.total()

    context = {"cart": cart_items, "items":total_items, "total":total_price}

    return render(request, template, context)

def qty_inc(request, pk):
    template = 'store/cart.html'

    #product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    order_item, created = OrderItem.objects.get_or_create(id=pk, cart=cart)#, product=product)
    order_item.quantity += 1
    order_item.save()

    return redirect('cart')

def qty_dec(request, pk):
    template = 'store/cart.html'

    #product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    order_item, created = OrderItem.objects.get_or_create(id=pk, cart=cart)#, product=product)
    order_item.quantity -= 1

    if order_item.quantity <= 0:
        order_item.delete()
    else:
        order_item.save()


    return redirect('cart')


def login(request):
    context = {}
    template = 'store/login.html'

    return render(request, template, context)


def signup(request):
    context = {}
    template = 'store/signup.html'
    #Customer()

    return render(request, template, context)



#response.user to get the current user details
