import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .forms import *
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Customer, Address, Product, ProductImages, Order, SoldItem
from store.decorators import authenticated_user, unauthenticated_user, allowed_users
from .decorators import not_seller
from .models import *
from django.http import JsonResponse
import json


# Create your views here.
@authenticated_user
def seller(request):
    template = 'seller/home.html'
    is_seller = False
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    addr = HomeAddress.objects.get(profile=seller)

    customer, created = Customer.objects.get_or_create(user=user)
    if customer.seller == True:
        is_seller = True
        group = Group.objects.get(name='seller')
        user.groups.add(group)
    else:
        is_seller = False

    context = {"isseller": is_seller, "profile": seller, "address": addr}

    return render(request, template, context)

@authenticated_user
def seller_profile(request):
    template = 'seller/profile.html'
    user = request.user
    seller = get_object_or_404(Profile, user=user)

    context = {"profile": seller}

    return render(request, template, context)


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
@allowed_users(allowed_roles=['seller'])
def create_product(request):
    template = 'seller/createproduct.html'
    created_product_success = ''
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    product_created = False

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
        context = {'productform': productform, "profile": seller, "created": product_created}
        print(context)

    return render(request, template, context)


def editproduct(request, pk): #make so that only the owner of the product can see this page
    template = 'seller/editproduct.html'
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    product = get_object_or_404(Product, id=pk)
    success = ''

    if request.method == "POST":
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
        #set the initial value of the fields to be populated with the product's details
        #so if they dont alter those fields the original value will be kept and no errors will arise
        editform = EditProduct(initial={'name': '%s' %product.name,
                                        'price': '%s' %product.price,
                                        'details': '%s' %product.details,
                                        'category':'%s' %product.category,
                                        'amt_available':'%s' %product.amt_available, })

    context = {"profile": seller, "editform": editform, "product": product}

    return render(request, template, context)

def delete_product(request, pk):
    template = 'seller/deleteproduct.html'
    product = get_object_or_404(Product, id=pk)
    user = request.user
    seller = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        answer = request.POST['verifydelete']
        if answer == 'yes':
            product.delete()
            messages.info(request, "Product deleted")
            return redirect('sellerproducts')
        if answer == 'no':
            return redirect('sellerproducts')
    else:
        context = {'product': product, 'profile': seller}
        return render(request, template, context)


def seller_paid(request):
    body = json.loads(request.body)
    product = get_object_or_404(Product, id=body['product_id'])
    product.paid = True
    product.save()

    return redirect('addimages')


def seller_products(request):
    template = 'seller/products.html'
    user = request.user
    seller = get_object_or_404(Profile, user=user)
    customer = get_object_or_404(Customer, user=user)

    if customer.seller == True:
        products = customer.product_set.all().order_by('-pub_date')
        paginator = Paginator(products, 6)

        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

        context = {"profile": seller, "page_obj": page_obj}

    return render(request, template, context)



def add_images(request):
    template = 'seller/addimages.html'
    customer = Customer.objects.get(user=request.user)
    seller_products = Product.objects.filter(product_seller=customer)
    user = request.user
    seller = get_object_or_404(Profile, user=user)

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

    context = {"profile": seller, 'imagesform': imagesform, 'userproducts': seller_products}
    return render(request, template, context)


def request_pickup(request):
    template = 'seller/pickup.html'

    user = request.user
    seller = get_object_or_404(Profile, user=user)

    context = {"profile": seller}

    return render(request, template, context)


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



def seller_sales(request):
    template = 'seller/sales.html'

    user = request.user
    customer = get_object_or_404(Customer, user=user)
    seller = get_object_or_404(Profile, user=user)
    solditems = SoldItem.objects.filter(seller=customer).order_by('-purchased_date')
    today = datetime.datetime.today()

    total = 0
    for item in solditems:
        total += item.total()

    context = {"profile": seller, "order_items": solditems, "total": total, "today": today}
    return render(request, template, context)


def payment_inquiries(request):
    template = 'seller/inquiries.html'

    user = request.user
    seller = get_object_or_404(Profile, user=user)

    context = {"profile": seller}

    return render(request, template, context)
