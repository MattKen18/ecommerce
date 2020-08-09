import datetime
from django.contrib import messages
from django.shortcuts import render
from .forms import AddressForm, PersonalForm, CreateProductForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Customer, Address, Product
from .models import *

# Create your views here.

def seller(request):
    template = 'seller/home.html'
    seller = False
    customer, created = Customer.objects.get_or_create(user=request.user)
    if customer.seller == True:
        seller = True
    else:
        seller = False

    if request.method == "POST":
        productform = CreateProductForm(request.POST, request.FILES)

        if productform.is_valid():
            return redirect('sellerhome')
    else:
        productform = CreateProductForm()

    context = {"seller": seller, 'productform': productform}


    return render(request, template, context)


def registerseller(request):
    template = 'seller/register.html'
    if request.method == "POST":
        addrform = AddressForm(request.POST)
        personalform = PersonalForm(request.POST)

        if addrform.is_valid() and personalform.is_valid():
            dob = personalform.cleaned_data['date_of_birth']
            gender = personalform.cleaned_data['gender']
            citz = personalform.cleaned_data['citizenship']

            try:
                profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                profile = Profile(user=request.user, date_of_birth=dob,
                                  gender=gender, citizenship=citz)
                profile.save()


            add1 = addrform.cleaned_data['address_line1']
            add2 = addrform.cleaned_data['address_line2']
            city = addrform.cleaned_data['city']
            state = addrform.cleaned_data['state']
            zip = addrform.cleaned_data['zip_code']
            country = addrform.cleaned_data['country']
            if (add1 and add2 and city and state and zip and country) == None:
                user_address, created = Address.objects.get_or_create(user=request.user)
                user_address.profile = profile
            else:
                user_address = HomeAddress(user=request.user, profile=profile, address_line1=add1, address_line2=add2,
                                           city=city, state=state, zip_code=zip, country=country)
                user_address.save()

            customer, created = Customer.objects.get_or_create(user=request.user)
            customer.seller = True

            customer.save()
            return redirect('sellerhome')

    else:
        addrform = AddressForm()
        personalform = PersonalForm()

    context = {"addrform": addrform, "personalform": personalform}
    return render(request, template, context)



def create_product(request):
    template = 'seller/home.html'
    created_product_success = ''

    if request.method == "POST":
        productform = CreateProductForm(request.POST, request.FILES)

    if productform.is_valid():

        name = productform.cleaned_data['name']
        price = productform.cleaned_data['price']
        details = productform.cleaned_data['details']
        category = productform.cleaned_data['category']
        condition = productform.cleaned_data['condition']
        amt_available = productform.cleaned_data['amt_available']
        #image = productform.cleaned_data['image']
        image = request.FILES['image']

        product_seller, created = Customer.objects.get_or_create(user=request.user)

        product = Product(product_seller=product_seller, name=name, price=price,
                      details=details, category=category, pub_date=datetime.datetime.now(),
                      image=image, condition=condition, amt_available=amt_available)
        product.save()

        created_product_success = messages.info(request, 'Product successfully created')
        return redirect('sellerhome')

    else:
        return redirect('shipping')
