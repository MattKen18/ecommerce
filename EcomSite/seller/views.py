import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .forms import *
from checkout.forms import ShippingForm
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Customer, Address, Product, ProductImages, Order, SoldItem, OrderItem
from store.decorators import authenticated_user, unauthenticated_user, allowed_users
from .decorators import not_seller, is_seller, profile_exists
from .models import *
from django.http import JsonResponse
import json
from store.context_processors import FEE

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


# Create your views here.
@authenticated_user
@is_seller
def seller(request):
    template = 'seller/home.html'
    is_seller = False
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    seller_customer = Customer.objects.get(user=user) #the only customer who can access this page must be the customer currently logged in as this is the seller home page
    seller_profile = Profile.objects.get(customer=seller_customer)
    seller_orders = SoldItem.objects.filter(seller=seller_customer).count()#completed orders made for this seller's (customer) products because customers can also be sellers if customer.seller is true
    seller_Products = Product.objects.filter(product_seller=seller_customer, re_evaluating=True).order_by("-req_date")[:4]

    addr = HomeAddress.objects.get(profile=seller)
    try:

        seller_recent_order = SoldItem.objects.filter(seller=seller_customer).order_by('-purchased_date')[0]
    except:
        seller_recent_order = ''

    customer, created = Customer.objects.get_or_create(user=user)
    if customer.seller == True:
        is_seller = True
        group = Group.objects.get(name='seller')
        user.groups.add(group)
    else:
        is_seller = False

    if request.method == "POST":
        inqform = Inquiries(request.POST)
        if inqform.is_valid():
            subject = inqform.cleaned_data['subject']
            details = inqform.cleaned_data['issue']

            subject_line = "%s - %s (%s)" %(user.username, subject, seller_profile.sellerid)
            email = EmailMessage(
                    subject_line,
                    details,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
            )
            email.fail_silently = True
            email.send()
            messages.info(request, "Your report has been recorded.")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        inqform = Inquiries()


    context = {"isseller": is_seller, "profile": seller, "address": addr, "sellerorders": seller_orders,
               "recent_sold": seller_recent_order, "sproducts": seller_Products, "inqform": inqform}

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
        userform = UserForm(request.POST)
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
                users = User.objects.all()
                usernames = [u.username for u in users]

                user.first_name = fname
                user.last_name = lname
                if uname not in usernames:
                    user.username = uname #check if username exists first
                elif uname == user.username:
                    pass
                else:
                    messages.error(request, "Username taken")
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                user.save()
                messages.info(request, "Profile Updated!")
            else:
                print('invalid')

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
    else:
        if form == "rempropic":
            image = Profile._meta.get_field('profile_pic').default #default profile pic
            profile.profile_pic = image #sets the image back to the default
            profile.save()
            messages.info(request, "Profile picture removed!")

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@authenticated_user
@not_seller
def registerseller(request):
    template = 'seller/register.html'
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == "POST":
        addrform = AddressForm(request.POST) #home address
        personalform = PersonalForm(request.POST)
        contactform = ContactForm(request.POST)
        miscform = MiscForm(request.POST)
        #propicform = ProPicForm(request.POST, request.FILES)

        if addrform.is_valid() and personalform.is_valid() and contactform.is_valid() and miscform.is_valid():

            add1 = addrform.cleaned_data['address_line1']
            add2 = addrform.cleaned_data['address_line2']
            city = addrform.cleaned_data['city']
            state = addrform.cleaned_data['state']
            zip = addrform.cleaned_data['zip_code']
            country = addrform.cleaned_data['country']
            print(country)

            if add1 == '' and add2 == '' and city == '' and state == '' and zip == '' and country == None:
                try:
                    shipping_addr = Address.objects.get(user=request.user) # tries to get the user's shipping address because they left the home address form empty
                except:
                    messages.info(request, "We don't have a shipping address for you, please give us your home address.")
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                else:
                    home_address = HomeAddress(user=request.user, address_line1=shipping_addr.address_line1, address_line2=shipping_addr.address_line2,
                                               city=shipping_addr.city, state=shipping_addr.state, zip_code=shipping_addr.zip_code, country=shipping_addr.country)

                    home_address.save()
                    messages.info(request, "We set your shipping address to also be your home address.")
            else:

                home_address = HomeAddress(user=request.user, address_line1=add1, address_line2=add2,
                                           city=city, state=state, zip_code=zip, country=country)
                                           #try addrform.save() instead of the above code
                home_address.save()

                try: #if the user completed the home address and doesn't have a shipping address
                    shipping_address = Address.objects.get(user=request.user) # tries to get the user's shipping address because they left the home address form empty
                except:
                    shipping_address = Address(user=request.user, address_line1=add1, address_line2=add2,
                                           city=city, state=state, zip_code=zip, country=country) #set the shipping address to the home address if the seller does not have a shipping address
                    shipping_address.save()


            dob = personalform.cleaned_data['date_of_birth']
            gender = personalform.cleaned_data['gender']

            phone = contactform.cleaned_data['phone']
            email = contactform.cleaned_data['email']

            note = miscform.cleaned_data['note']

            if note == None:
                note = ''

            try:
                profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=request.user, date_of_birth=dob,
                                  gender=gender, phone=phone, customer=customer,
                                  email=email, note=note, tier="T0")#initially sets the seller tier to tier 0
                profile.save()

                try:
                    home_address = get_object_or_404(HomeAddress, user=request.user)
                    home_address.profile = profile #a profile is set to a shipping address model if the seller did not set his/her homeaddress
                    home_address.save()
                except:
                    pass

                try:
                    shipping_address = get_object_or_404(Address, user=request.user)
                    shipping_address.profile = profile
                    shipping_address.save()
                except:
                    pass

            else:
                profile.phone = phone
                profile.email = email
                profile.save()


                customer = get_object_or_404(Customer, user=request.user)
                customer.seller = True
                customer.save()

                messages.info(request, "You're already a seller")
                return redirect('sellerhome')

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

            product_seller = get_object_or_404(Customer, user=user)

            product = Product(product_seller=product_seller, name=name, price=price,
                          details=details, category=category, req_date=datetime.datetime.now(),
                          image=image, condition=condition, amt_available=amt_available)
            product.save()
            product_created = True
            created_product_success = messages.info(request, 'Product successfully created')
            return redirect('addimages', product.id, "paystream")
            #return redirect('addimages')#'sellerhome')

    else:
        productform = CreateProductForm()

    try:
        context = {'productform': productform, "profile": seller, "created": product_created, "product": product}
        #print(context)
    except:
        context = {'productform': productform, "profile": seller, "created": product_created, "address": addr}
        #print(context)

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
                product.req_date = datetime.datetime.now()
                product.re_evaluating = True
                product.published = False
                product.verified = False
                product.edited = True
                product.save()

                messages.info(request, "Product was successfully updated! Your product will be evaluated and re-published if deemed fit.")
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
                                        'category':'%s' %product.category, })

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
    customer = get_object_or_404(Customer, user=user)

    if request.method == "POST":
        answer = request.POST['verifydelete']
        if product.product_seller == customer:
            if answer == 'yes':
                product.delete()
                messages.info(request, "Product deleted")
                return redirect('sellerproducts')
            if answer == 'no':
                return redirect('sellerproducts')
        else:
            messages.info(request, "Don't be sneeky, that's not your product :-P")
            return redirect('store')
    else:
        context = {'product': product, 'profile': seller, "address": addr}
        return render(request, template, context)


@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def product_payment(request, pk):
    template = "seller/productpay.html"
    customer = get_object_or_404(Customer, user=request.user)
    product = get_object_or_404(Product, id=pk)
    seller_products = Product.objects.filter(product_seller=customer)
    info = ''
    if product in seller_products:
        if product.paid == True:
            info = messages.info(request, "Payment fee for product is already paid.")
            return redirect("sellerhome")
        else:
            total = product.amt_available * FEE #payment fee of ChegBase ($100 JMD)
    else:
        info = messages.info(request, "That's not your product!")
        return redirect('sellerhome')

    context = {"product": product, "total": total}
    return render(request, template, context)

@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def seller_paid(request):
    body = json.loads(request.body)
    product = get_object_or_404(Product, id=body['product_id'])
    product.paid = True
    product.save()

    return redirect('addimages', product.id, "view")

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
def restock(request):
    template = 'seller/restock.html'

    user = request.user
    seller = get_object_or_404(Profile, user=user)
    customer = get_object_or_404(Customer, user=user)
    addr = HomeAddress.objects.get(profile=seller)

    if customer.seller == True:
        products = customer.product_set.all().filter(available=False).order_by('-pub_date') #amt_available__lte=0,
        paginator = Paginator(products, 6)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        context = {"profile": seller, "page_obj": page_obj, "address": addr}
    else:
        return redirect('registerseller')

    return render(request, template, context)

@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def add_images(request, pk, mode): #adding images from paystream #product will not be set to edited or re-evaluating
    template = 'seller/addimages.html'
    customer = Customer.objects.get(user=request.user)
    seller_products = Product.objects.filter(product_seller=customer)
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    addr = HomeAddress.objects.get(profile=seller)
    product = Product.objects.get(id=pk) #the product just created by the create product view
    product_sec_images = ProductImages.objects.filter(product=product) #secondary images for the product
    paystream = False #if accessing from create product to add images then this would be True
    modify = False

    if product in seller_products:
        if request.method == 'POST':
            imagesform = AddSecondaryImages(request.POST, request.FILES)
            primageform = AddPrimaryImage(request.POST, request.FILES)

            if mode == "secondary":
                if imagesform.is_valid():

                    image = request.FILES.get('image')
                    extraimages, created = ProductImages.objects.get_or_create(product=product, image=image)
                    product.published = False
                    product.verified = False
                    product.save()
                    messages.info(request, 'Secondary Image added')
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            elif mode == "primary":
                if primageform.is_valid():

                    image = request.FILES.get('primaryimage')
                    product.image = image
                    product.verified = False
                    product.published = False
                    product.save()
                    messages.info(request, 'Primary image updated')
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            imagesform = AddSecondaryImages()
            primageform = AddPrimaryImage()

        context = {"profile": seller, 'imagesform': imagesform, 'userproducts': seller_products,
                   "address": addr, "secondaryimages": product_sec_images, "product": product,
                   "primageform": primageform}
    else:
        info = messages.info(request, "That's not your product!")
        return redirect('sellerhome')

    return render(request, template, context)



@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def add_images_after(request, pk, mode): #adding images from sellerhome #product will be set to edited and re-evaluating
    template = 'seller/addimagesafter.html'
    customer = Customer.objects.get(user=request.user)
    seller_products = Product.objects.filter(product_seller=customer)
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    addr = HomeAddress.objects.get(profile=seller)
    product = Product.objects.get(id=pk) #the product just created by the create product view
    product_sec_images = ProductImages.objects.filter(product=product) #secondary images for the product

    if product in seller_products:
        if request.method == 'POST':
            imagesform = AddSecondaryImages(request.POST, request.FILES)
            primageform = AddPrimaryImage(request.POST, request.FILES)

            if mode == "secondary":
                if imagesform.is_valid():

                    image = request.FILES.get('image')
                    extraimages, created = ProductImages.objects.get_or_create(product=product, image=image)
                    product.edited = True
                    product.published = False
                    product.verified = False
                    product.re_evaluating = True
                    product.save()
                    messages.info(request, 'Secondary Image added')
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            elif mode == "primary":
                if primageform.is_valid():

                    image = request.FILES.get('primaryimage')
                    product.image = image
                    product.edited = True
                    product.verified = False
                    product.published = False
                    product.re_evaluating = True
                    product.save()
                    messages.info(request, 'Primary image updated')
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            imagesform = AddSecondaryImages()
            primageform = AddPrimaryImage()

        context = {"profile": seller, 'imagesform': imagesform, 'userproducts': seller_products,
                   "address": addr, "secondaryimages": product_sec_images, "product": product,
                   "primageform": primageform}
    else:
        info = messages.info(request, "That's not your product!")
        return redirect('sellerhome')

    return render(request, template, context)




@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def delete_image(request, pk):
    image = ProductImages.objects.get(id=pk)
    image.delete()

    messages.info(request, 'Secondary Image removed')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


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
    customer = get_object_or_404(Customer, user=user)
    profile = get_object_or_404(Profile, customer=customer)

    if request.method == "POST":
        location = request.POST["location"]
        date = request.POST["date"]
        time = request.POST["time"]
        phone = request.POST["phone"]

        pickup = Pickup.objects.create(user=user, location=location, date=date, time=time, phone=phone)
        messages.info(request, "We'll Be There!")

        template = render_to_string('checkout/restock_email_template.html', {'name': user.username,
                                                                    'location': location, 'date': date,
                                                                    'time': time, 'phone': phone})
        email = EmailMessage(
                "Pickup for %s (%s)" %(user.username, profile.sellerid),
                template,
                settings.EMAIL_HOST_USER,
                [profile.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('pickup')




@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def seller_sales(response):
    template = 'seller/sales.html'

    user = response.user
    customer = get_object_or_404(Customer, user=user)
    seller = get_object_or_404(Profile, user=user)
    solditems = SoldItem.objects.filter(seller=customer).order_by('-purchased_date')
    seller_products = Product.objects.filter(product_seller=customer)

    today = datetime.datetime.today()
    addr = HomeAddress.objects.get(profile=seller)

    paginator = Paginator(solditems, 5)

    page_number = response.GET.get('page')

    page_obj = paginator.get_page(page_number)


    total = 0
    for item in solditems:
        total += item.total()

    context = {"profile": seller, "order_items": solditems, "total": total,
               "today": today, "address": addr, 'page_obj': page_obj}

    return render(response, template, context)

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
        tier = (100 * solditems) + (10 * seller.vouches_amt())
        return tier


    if seller.user == user: #checks if the person trying to vouch for the seller is the actual seller
        messages.info(request, "You can't vouch for yourself")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) #this returns to the current page
    elif customer in seller_vouches: #checks if the customer already vouched for this seller
        messages.info(request, "You already vouched for this seller")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else: #customer who isn't the seller and has not already vouched for this seller
        seller.vouches.add(customer)
        seller.save()

        tier_points = tierCalc()
        seller.tier_points = tier_points
        seller.save()

        # this if else block sets the tier the seller should be in based on their tier_points
        if tier_points >= TIER_3:
            seller.tier = "T3"
        elif tier_points < TIER_3 and tier_points >= TIER_2:
            seller.tier = "T2"
        else:
            seller.tier = "T1"

        seller.save()

        messages.info(request, "You vouched for " + seller.user.username + "!" )
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@authenticated_user
@is_seller
@allowed_users(allowed_roles=['seller', 'staff'])
def restock_product(request, pk):
    template = "seller/restockproduct.html"
    product = Product.objects.get(id=pk)
    customer = get_object_or_404(Customer, user=request.user)

    if product.product_seller == customer:
        if request.method == "POST":
            restockform = Restock(request.POST)

            if restockform.is_valid():
                amt = restockform.cleaned_data['amt_available']
                if int(amt) <= 0:
                    messages.info(request, "Invalid quantity!")
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                else:
                    product.amt_available = amt
                    product.req_date = datetime.datetime.now()
                    product.re_evaluating = True
                    product.published = False
                    product.verified = False
                    product.restocking = True #sent for restocking in AdminVerify
                    product.save()
                    messages.info(request, "Success! Please await stock verification")
                    return redirect('restockproducts')

        else:
            restockform = Restock(initial={"amt_available": "%s" %product.amt_available})

    else:
        messages.info(request, "Don't be sneeky, that's not your product :-P")
        return redirect('store')

    context = {"restockform": restockform, "product": product}

    return render(request, template, context)

@authenticated_user
def profileview(request, pk, username): #when clicking on a seller's profile
    template = "seller/profileview.html"
    customer = get_object_or_404(Customer, id=pk)
    seller = get_object_or_404(Profile, customer=customer)
    home_address = HomeAddress.objects.get(profile=seller)
    seller_products = Product.objects.all().filter(product_seller=customer, published=True,
                                                   restocking=False, edited=False,
                                                   re_evaluating=False, verified=True,
                                                   available=True, paid=True).order_by("-pub_date")
    seller_products_4 = seller_products[:4]

    more = False #show more link on page
    if seller_products.count() > 4:
        more = True
    else:
        more = False

    context = {"seller": seller, "homeaddress": home_address, "products": seller_products_4,
               "more": more, "customer": customer}

    return render(request, template, context)

@authenticated_user
@profile_exists
def personalprofileview(request, pk, username): #when viewing myprofile
    template = "seller/profileview.html"
    customer = get_object_or_404(Customer, id=pk)
    seller = get_object_or_404(Profile, customer=customer)
    home_address = HomeAddress.objects.get(profile=seller)
    seller_products = Product.objects.all().filter(product_seller=customer, published=True,
                                                   restocking=False, edited=False,
                                                   re_evaluating=False, verified=True,
                                                   available=True, paid=True).order_by("-pub_date")
    seller_products_4 = seller_products[:4]

    more = False #show more link on page
    if seller_products.count() > 4:
        more = True
    else:
        more = False

    context = {"seller": seller, "homeaddress": home_address, "products": seller_products_4,
               "more": more, "customer": customer}

    return render(request, template, context)


@authenticated_user
def profile_seller_products(request, pk, username):
    template = "seller/sellerproducts.html"
    customer = get_object_or_404(Customer, id=pk)
    seller = get_object_or_404(Profile, customer=customer)
    seller_products = Product.objects.all().filter(product_seller=customer, published=True,
                                                   restocking=False, edited=False,
                                                   re_evaluating=False, verified=True,
                                                   available=True, paid=True).order_by("-pub_date")

    paginator = Paginator(seller_products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"products": seller_products, "page_obj": page_obj, "customer": customer}
    return render(request, template, context)
