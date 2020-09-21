from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import *
from seller.models import Profile

FEE = 100 #cost per item (product fee)

def send_to_main(request): #use this to add context variables available to all templates
    template = 'store/main.html'
    user = request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = OrderItem.objects.filter(cart=cart)
        total_items = cart_items.count()

        customer = get_object_or_404(Customer, user=user)
        cart_order_items = OrderItem.objects.filter(cart=cart)

        cart_total = 0
        for item in cart_order_items:
            cart_total += item.total()

        if customer.seller == True:
            profile  = get_object_or_404(Profile, user=user)
            context = {"fee": FEE, "cart": cart_order_items, "cartquantity": total_items, "profile": profile, "cart_total": cart_total}
        else:
            context = {"fee": FEE, "cart": cart_order_items, "cartquantity": total_items, "cart_total": cart_total}

        return context
    else:
        return ''
