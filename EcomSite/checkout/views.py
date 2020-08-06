from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ShippingForm
from store.models import Address, Cart, OrderItem

# Create your views here.

def shipping(request):
    template = 'checkout/shipping.html'
    if request.method == "POST":
        shipform = ShippingForm(request.POST)

        if shipform.is_valid():
            add1 = shipform.cleaned_data['address_line1']
            add2 = shipform.cleaned_data['address_line2']
            state = shipform.cleaned_data['state']
            zip = shipform.cleaned_data['zip_code']
            country = shipform.cleaned_data['country']

            try:
                Address.objects.get(user=request.user)
                addr_already_exists = messages.error(request, 'We already have an address for you.')
                return redirect('shipping')
                addr_already_exists = ''
            except:
                user_address = Address(user=request.user, address_line1=add1, address_line2=add2, state=state, zip_code=zip, country=country)
                user_address.save()

                return redirect('checkout')

    else:
        shipform = ShippingForm()

    context = {"shipform": shipform}

    return render(request, template, context)


#def create_shipping_info(request):
#    template = 'checkout/shipping.html'
#    context = {}

#    return render(request, template, context)

def checkout(request):
    template = 'checkout/checkout.html'
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = OrderItem.objects.filter(cart=cart)
    address = Address.objects.get(user=request.user)

    context = {"order_items": cart_items, "address": address}

    return render(request, template, context)
