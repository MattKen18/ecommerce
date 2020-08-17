from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShippingForm
from store.models import Address, Cart, OrderItem, SingleBuy, Customer
from store.decorators import authenticated_user, unauthenticated_user
# Create your views here.

@authenticated_user
def shipping(request):
    template = 'checkout/shipping.html'
    if request.method == "POST":
        shipform = ShippingForm(request.POST)

        if shipform.is_valid():
            add1 = shipform.cleaned_data['address_line1']
            add2 = shipform.cleaned_data['address_line2']
            state = shipform.cleaned_data['state']
            city = shipform.cleaned_data['city']
            zip = shipform.cleaned_data['zip_code']
            country = shipform.cleaned_data['country']

            try:
                Address.objects.get(user=request.user)
                addr_already_exists = messages.error(request, 'We already have an address for you.')
                return redirect('shipping')
                addr_already_exists = ''
            except:
                user_address = Address(user=request.user, address_line1=add1, address_line2=add2, city=city, state=state, zip_code=zip, country=country)
                user_address.save()

                return redirect('checkout')

    else:
        shipform = ShippingForm()

    address_exists = True
    try:
        Address.objects.get(user=request.user)
    except:
        address_exists = False
    else:
        address_exists = True

    context = {"shipform": shipform, "address": address_exists}

    return render(request, template, context)


#def create_shipping_info(request):
#    template = 'checkout/shipping.html'
#    context = {}

#    return render(request, template, context)

@authenticated_user
def checkout(request):
    template = 'checkout/checkout.html'

    try:
        customer = Customer.objects.get(user=request.user)
        singles = SingleBuy.objects.filter(customer=customer)
        address = Address.objects.get(user=request.user)
    except:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = OrderItem.objects.filter(cart=cart)
        address = Address.objects.get(user=request.user)
        context = {"address": address, "order_items": cart_items}

    else:
        if singles.count() == 0:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = OrderItem.objects.filter(cart=cart)
            address = Address.objects.get(user=request.user)
            context = {"address": address, "order_items": cart_items}
        else:
            context = {"address": address, "single": singles}



    return render(request, template, context)
