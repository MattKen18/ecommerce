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

def cart(response):
    template = 'store/cart.html'
    context = {}

    return render(request, template, context)

def checkout(request):
    template = 'store/checkout.html'
    context = {}
    return render(request, template, context)

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
