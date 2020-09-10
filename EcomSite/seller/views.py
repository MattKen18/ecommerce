import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .forms import *
from checkout.forms import ShippingForm
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Customer, Address, Product, ProductImages, Order, SoldItem
from store.decorators import authenticated_user, unauthenticated_user, allowed_users
from .decorators import not_seller, is_seller
from .models import *
from django.http import JsonResponse
import json


# Create your views here.
@authenticated_user
@is_seller
def seller(request):
    template = 'seller/home.html'
    is_seller = False
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    seller_customer = Customer.objects.get(user=user) #the only customer who can access this page must be the customer currently logged in as this is the seller home page
    seller_orders = SoldItem.objects.filter(seller=seller_customer).count()#completed orders made for this seller's (customer) products because customers can also be sellers if customer.seller is true
    addr = HomeAddress.objects.get(profile=seller)

    customer, created = Customer.objects.get_or_create(user=user)
    if customer.seller == True:
        is_seller = True
        group = Group.objects.get(name='seller')
        user.groups.add(group)
    else:
        is_seller = False

    context = {"isseller": is_seller, "profile": seller, "address": addr, "sellerorders": seller_orders}

    return render(request, template, context)

@authenticated_user
@is_seller
def seller_profile(request):
    template = 'seller/profile.html'
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    homeaddr, created = HomeAddress.objects.get_or_create(user=user)
    shippingaddr, created = Address.objects.get_or_create(user=user)

    if request.method == "POST":
        addrform = AddressForm(request.POST)
        shipaddr = ShippingForm(request.POST)
        personalform = PersonalForm(request.POST)
        contactform = ContactForm(request.POST)
        miscform = MiscForm(request.POST)
        propicform = ProPicForm(request.POST, request.FILES)

    else:
        addrform = AddressForm(initial={"address_line1": "%s" %homeaddr.address_line1,
                                        "address_line2": "%s" %homeaddr.address_line2,
                                        "city": "%s" %homeaddr.city,
                                        "state": "%s" %homeaddr.state,
                                        "zip_code": "%s" %homeaddr.zip_code,
                                        "country": "%s" %homeaddr.country,})
        shipaddr = ShippingForm(initial={"address_line1": "%s" %shippingaddr.address_line1,
                                        "address_line2": "%s" %shippingaddr.address_line2,
                                        "city": "%s" %shippingaddr.city,
                                        "state": "%s" %shippingaddr.state,
                                        "zip_code": "%s" %shippingaddr.zip_code,
                                        "country": "%s" %shippingaddr.country,})
        personalform = PersonalForm(initial={"date_of_birth": "%s" % seller.date_of_birth,
                                             "gender": "%s" % seller.gender})
        contactform = ContactForm(initial={"email": "%s" % seller.email,
                                           "phone": "%s" % seller.phone })
        userform = UserForm(initial={"first_name": "%s" % user.first_name,
                                     "last_name": "%s" % user.last_name,
                                     "username": "%s" % user.username,})
        if seller.note != None:
            miscform = MiscForm(initial={"note": "%s" % seller.note})
        else:
            miscform = MiscForm()
        propicform = ProPicForm()

    context = {"profile": seller, "homeaddrform": addrform, "shippingaddr": shipaddr,
               "personalform": personalform, "contactform": contactform,
               "miscform": miscform, "propicform": propicform, "userform": userform}

    return render(request, template, context)

@authenticated_user
@is_seller
def update_seller_profile(request, form):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    homeaddress, created = HomeAddress.objects.get_or_create(user=user)
    shippingaddress, created = Address.objects.get_or_create(user=user)

    if request.method == "POST":
        homeaddr = AddressForm(request.POST)
        shipaddr = ShippingForm(request.POST)
        personalform = PersonalForm(request.POST)
        contactform = ContactForm(request.POST)
        miscform = MiscForm(request.POST)
        propicform = ProPicForm(request.POST, request.FILES)
        userform = UserForm(request.POST)

        if form == 'user':
            if userform.is_valid():
                fname = userform.cleaned_data['first_name']
                lname = userform.cleaned_data['last_name']
                uname = userform.cleaned_data['username']

                user.first_name = fname
                user.last_name = lname
                user.username = uname
                user.save()
                messages.info(request, "Profile Updated!")

        if form == 'personal':
            if personalform.is_valid():
                dob = personalform.cleaned_data['date_of_birth']
                gender = personalform.cleaned_data['gender']

                profile.date_of_birth = dob
                profile.gender = gender
                profile.save()
                messages.info(request, "Profile Updated!")

        if form == 'contact':
            if contactform.is_valid():
                email = contactform.cleaned_data['email']
                phone = contactform.cleaned_data['phone']

                profile.email = email
                profile.phone = phone
                profile.save()
                messages.info(request, "Profile Updated!")

        if form == 'homeaddress':
            if homeaddr.is_valid():
                adl1 = homeaddr.cleaned_data['address_line1']
                adl2 = homeaddr.cleaned_data['address_line2']
                city = homeaddr.cleaned_data['city']
                state = homeaddr.cleaned_data['state']
                zip = homeaddr.cleaned_data['zip_code']
                country = homeaddr.cleaned_data['country']

                homeaddress.address_line1 = adl1
                homeaddress.address_line2 = adl2
                homeaddress.city = city
                homeaddress.state = state
                homeaddress.zip_code = zip
                homeaddress.country = country

                homeaddress.save()
                messages.info(request, "Home Address Updated!")

        if form == 'shippingaddress':
            if shipaddr.is_valid():
                adl1 = shipaddr.cleaned_data['address_line1']
                adl2 = shipaddr.cleaned_data['address_line2']
                city = shipaddr.cleaned_data['city']
                state = shipaddr.cleaned_data['state']
                zip = shipaddr.cleaned_data['zip_code']
                country = shipaddr.cleaned_data['country']

                shippingaddress.address_line1 = adl1
                shippingaddress.address_line2 = adl2
                shippingaddress.city = city
                shippingaddress.state = state
                shippingaddress.zip_code = zip
                shippingaddress.country = country

                shippingaddress.save()
                messages.info(request, "Shipping Address Updated!")

        if form =='propic':
            if propicform.is_valid():
                propic = request.FILES.get('profile_pic')

                profile.profile_pic = propic
                profile.save()
                messages.info(request, "Profile picture Updated!")

        if form == 'miscnote':
            if miscform.is_valid():
                note = miscform.cleaned_data['note']
                print(note)
                profile.note = note
                profile.save()
                messages.info(request, "Seller's note Updated!")
            else:
                print("not")

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@authenticated_user
@not_seller
def registerseller(request):
    template = 'seller/register.html'

    if request.method == "POST":
        addrform = AddressForm(request.POST)
        personalform = PersonalForm(request.POST)
        contactform = ContactForm(request.POST)
        miscform = MiscForm(request.POST)
        #propicform = ProPicForm(request.POST, request.FILES)

        if addrform.is_valid() and personalform.is_valid() and contactform.is_valid() and miscform.is_valid():
            dob = personalform.cleaned_data['date_of_birth']
            gender = personalform.cleaned_data['gender']

            phone = contactform.cleaned_data['phone']
            email = contactform.cleaned_data['email']

            business = miscform.cleaned_data['business']

            try:
                profile = Profile.objects.get(user=request.user)

            except Profile.DoesNotExist:
                profile = Profile(user=request.user, date_of_birth=dob,
                                  gender=gender, phone=phone,
                                  email=email, business=business)
                profile.save()

            else:
                profile.phone = phone
                profile.email = email
                profile.business = business

                profile.save()

                customer = get_object_or_404(Customer, user=request.user)
                customer.seller = True
                customer.save()

                messages.info(request, "You're already a seller")
                return redirect('sellerhome')


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
                print(user_address.country)

            customer = get_object_or_404(Customer, user=request.user)
            customer.seller = True

            customer.save()

            return redirect('profilepic')

    else:
        addrform = AddressForm()
        personalform = PersonalForm(initial={"Country": "Jamaica"})
        contactform = ContactForm(initial={"email": "%s" % request.user.email})
        miscform = MiscForm()

    context = {"addrform": addrform, "personalform": personalform,
               "contactform": contactform, "miscform": miscform}

    return render(request, template, context)

@authenticated_user
@is_seller
def upload_profilepic(request):
    template = 'seller/profilepic.html'
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        propicform = ProPicForm(request.POST, request.FILES)

        if propicform.is_valid():
            profile_pic = request.FILES.get('profile_pic')

            profile.profile_pic = profile_pic
            profile.save()
            #return redirect('sellerhome')
            messages.info(request, "Profile image successfully updated")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    else:
        propicform = ProPicForm()

    context = {'profile': profile, 'propicform': propicform}
    return render(request, template, context)

@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller'])
def create_product(request):
    template = 'seller/createproduct.html'
    created_product_success = ''
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    product_created = False
    addr = HomeAddress.objects.get(profile=seller)

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
            image = request.FILES.get('image')

            product_seller, created = Customer.objects.get_or_create(user=user)

            product = Product(product_seller=product_seller, name=name, price=price,
                          details=details, category=category, req_date=datetime.datetime.now(),
                          image=image, condition=condition, amt_available=amt_available)
            product.save()
            product_created = True
            created_product_success = messages.info(request, 'Product successfully created')
            #return redirect('addimages')#'sellerhome')

    else:
        productform = CreateProductForm()

    try:
        context = {'productform': productform, "profile": seller, "created": product_created, "product": product}
        print(context)
    except:
        context = {'productform': productform, "profile": seller, "created": product_created, "address": addr}
        print(context)

    return render(request, template, context)


@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def editproduct(request, pk): #make so that only the owner of the product can see this page //#fixed#//
    template = 'seller/editproduct.html'
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    product = get_object_or_404(Product, id=pk)
    customer = get_object_or_404(Customer, user=user)
    addr = HomeAddress.objects.get(profile=seller)


    if request.method == "POST":
        if product.product_seller == customer:
            editform = EditProduct(request.POST)
            if editform.is_valid():
                name = editform.cleaned_data['name']
                price = editform.cleaned_data['price']
                details = editform.cleaned_data['details']
                category = editform.cleaned_data['category']
                condition = editform.cleaned_data['condition']
                amt_available = editform.cleaned_data['amt_available']
                #image = productform.cleaned_data['image']
                image = request.FILES.get('image')
                if image not in ['', None]: #if no image is selected
                    product.image = image
                else:
                    product.image = product.image #use the products image

                product.name = name
                product.price = price
                product.details = details
                product.category = category
                product.condition = condition
                product.amt_available = amt_available
                product.req_date = datetime.datetime.now()
                product.re_evaluating = True
                product.published = False
                product.verified = False
                product.save()

                messages.info(request, "Product was successfully updated. Your product will be evaluated and re-published if deemed fit.")
                return redirect('editproduct', pk=pk)
        else:
            messages.info(request, "Don't be sneeky, that's not your product :-P")
            return redirect('store')

    else:
        #set the initial value of the fields to be populated with the product's details
        #so if they dont alter those fields the original value will be kept and no errors will arise
        editform = EditProduct(initial={'name': '%s' %product.name,
                                        'price': '%s' %product.price,
                                        'details': '%s' %product.details,
                                        'category':'%s' %product.category,
                                        'amt_available':'%s' %product.amt_available, })

    context = {"profile": seller, "editform": editform, "product": product, "address": addr}

    return render(request, template, context)


@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def delete_product(request, pk):
    template = 'seller/deleteproduct.html'
    product = get_object_or_404(Product, id=pk)
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    addr = HomeAddress.objects.get(profile=seller)


    if request.method == "POST":
        answer = request.POST['verifydelete']
        if answer == 'yes':
            product.delete()
            messages.info(request, "Product deleted")
            return redirect('sellerproducts')
        if answer == 'no':
            return redirect('sellerproducts')
    else:
        context = {'product': product, 'profile': seller, "address": addr}
        return render(request, template, context)


@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def seller_paid(request):
    body = json.loads(request.body)
    product = get_object_or_404(Product, id=body['product_id'])
    product.paid = True
    product.save()

    return redirect('addimages')

@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def seller_products(request):
    template = 'seller/products.html'
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    customer = get_object_or_404(Customer, user=user)
    addr = HomeAddress.objects.get(profile=seller)



    if customer.seller == True:
        products = customer.product_set.all().order_by('-pub_date')
        paginator = Paginator(products, 6)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        context = {"profile": seller, "page_obj": page_obj, "address": addr}

    return render(request, template, context)

@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def restock_products(request):
    template = 'seller/restock.html'

    user = request.user
    seller = get_object_or_404(Profile, user=user)
    customer = get_object_or_404(Customer, user=user)
    addr = HomeAddress.objects.get(profile=seller)

    if customer.seller == True:
        products = customer.product_set.all().filter(amt_available__lte=0).order_by('-pub_date')
        paginator = Paginator(products, 6)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        context = {"profile": seller, "page_obj": page_obj, "address": addr}

    return render(request, template, context)

@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def add_images(request):
    template = 'seller/addimages.html'
    customer = Customer.objects.get(user=request.user)
    seller_products = Product.objects.filter(product_seller=customer)
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    addr = HomeAddress.objects.get(profile=seller)


    if request.method == 'POST':
        imagesform = AddSecondaryImages(request.POST, request.FILES)

        if imagesform.is_valid():
            product_id = request.POST['productchoice']
            product = Product.objects.get(pk=product_id)

            image = request.FILES.get('image')

            extraimages, created = ProductImages.objects.get_or_create(product=product, image=image)

            images_updated = messages.info(request, 'images updated')
            return redirect('addimages')

    else:
        imagesform = AddSecondaryImages()

    context = {"profile": seller, 'imagesform': imagesform, 'userproducts': seller_products, "address": addr}
    return render(request, template, context)


@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def request_pickup(request):
    template = 'seller/pickup.html'
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    addr = HomeAddress.objects.get(profile=seller)


    context = {"profile": seller, "address": addr}

    return render(request, template, context)

@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def pickup(request):
    user = request.user

    if request.method == "POST":
        location = request.POST["location"]
        date = request.POST["date"]
        time = request.POST["time"]
        phone = request.POST["phone"]

        pickup = Pickup.objects.create(user=user, location=location, date=date, time=time, phone=phone)
        messages.info(request, "We'll Be There!")
        return redirect('pickup')


@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def seller_sales(request):
    template = 'seller/sales.html'

    user = request.user
    customer = get_object_or_404(Customer, user=user)
    seller = get_object_or_404(Profile, user=user)
    solditems = SoldItem.objects.filter(seller=customer).order_by('-purchased_date')
    today = datetime.datetime.today()
    addr = HomeAddress.objects.get(profile=seller)

    total = 0
    for item in solditems:
        total += item.total()

    context = {"profile": seller, "order_items": solditems, "total": total, "today": today, "address": addr}
    return render(request, template, context)

@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def payment_inquiries(request):
    template = 'seller/inquiries.html'

    user = request.user
    seller = get_object_or_404(Profile, user=user)
    addr = HomeAddress.objects.get(profile=seller)

    context = {"profile": seller, "address": addr}

    return render(request, template, context)



# HAVE A TIER CHECK AND UPDGRADE FUNCTION THAT CAN BE REUSED
@authenticated_user
def vouch(request, pk):
    user = request.user
    seller = get_object_or_404(Profile, sellerid=pk) #seller the user wants to vouch for
    seller_customer = get_object_or_404(Customer, user=seller.user) #the customer profile of the seller /the seller
    customer = get_object_or_404(Customer, user=user) #current customer/user /not the seller
    seller_vouches = seller.vouches.all() #all the vouches of the seller i.e all the customers who vouched for seller
    solditems = SoldItem.objects.filter(seller=seller_customer).count() #amt of items sold by seller

    def tierCalc(): #calculates the tierPoints which determine what tier the seller should be in
        tier = (0.7 * solditems) + (0.3 * seller.vouches_amt())
        return tier

    # threshold of each tier
    tier1 = 10
    tier2 = 50
    tier3 = 100


    if seller.user == user: #checks if the person trying to vouch for the seller is the actual seller
        messages.info(request, "You can't vouch for youself")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) #this returns to the current page
    elif customer in seller_vouches: #checks if the customer already vouched for this seller
        messages.info(request, "You already vouched for this seller")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else: #customer who isn't the seller and has not already vouched for this seller
        seller.vouches.add(customer)
        seller.save()

        tier_points = tierCalc()

        # this if else block sets the tier the seller should be in based on their tier_points
        if tier_points >= tier3:
            seller.tier = "T3"
        elif tier_points < tier3 and tier_points >= tier2:
            seller.tier = "T2"
        elif tier_points < tier2 and tier_points >= tier1:
            seller.tier = "T1"
        else:
            seller.tier = "T0"

        seller.save()

        print(seller.tier)
        messages.info(request, "You vouched for " + seller.user.username + "!" )
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
