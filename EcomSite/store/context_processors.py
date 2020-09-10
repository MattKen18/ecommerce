from django.contrib.auth.models import User
from .models import *

def send_to_main(request): #use this to add context variables available to all templates
    template = 'store/main.html'
    user = request.user
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = OrderItem.objects.filter(cart=cart)
        total_items = cart_items.count()

        context = {"cartquantity": total_items}

        return context
    else:
        return ''
