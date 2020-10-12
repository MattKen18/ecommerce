import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from store.models import Product, ProductImages, categories, conditions
from seller.models import Profile
from .forms import ImageUpload
from store.decorators import allowed_users
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.

@allowed_users(allowed_roles=['staff'])
def admin_verify(request):
    template = 'adminverify/baseverify.html'

    unverified = Product.objects.all().filter(published=False).order_by('-req_date')
    categories = Product._meta.get_field('category').choices
    conditions = Product._meta.get_field('condition').choices

    if request.method == "POST":
        imageform = ImageUpload(request.POST)
    else:
        imageform = ImageUpload()

    context = {'products': unverified, 'categories': categories, 'conditions': conditions, 'imageform': imageform}
    return render(request, template, context)


@allowed_users(allowed_roles=['staff'])
def verify_new(request):
    template = "adminverify/newproductsverify.html"
    unverified = Product.objects.all().filter(published=False, re_evaluating=False, edited=False).order_by('-req_date')
    categories = Product._meta.get_field('category').choices
    conditions = Product._meta.get_field('condition').choices

    if request.method == "POST":
        imageform = ImageUpload(request.POST)
    else:
        imageform = ImageUpload()

    context = {'products': unverified, 'categories': categories, 'conditions': conditions, 'imageform': imageform}
    return render(request, template, context)

@allowed_users(allowed_roles=['staff'])
def re_evaluate(request):
    template = "adminverify/re_evaluate.html"
    unverified = Product.objects.all().filter(published=False, re_evaluating=True, edited=True, restocking=False).order_by('-req_date')
    categories = Product._meta.get_field('category').choices
    conditions = Product._meta.get_field('condition').choices

    if request.method == "POST":
        imageform = ImageUpload(request.POST)
    else:
        imageform = ImageUpload()

    context = {'products': unverified, 'categories': categories, 'conditions': conditions, 'imageform': imageform}
    return render(request, template, context)

@allowed_users(allowed_roles=['staff'])
def re_stock(request):
    template = 'AdminVerify/restockingproducts.html'
    restocking_products = Product.objects.filter(published=False, re_evaluating=True, restocking=True, edited=False).order_by('-req_date')
    categories = Product._meta.get_field('category').choices
    conditions = Product._meta.get_field('condition').choices

    context = {'products': restocking_products, 'categories': categories, 'conditions': conditions}

    return render(request, template, context)


@allowed_users(allowed_roles=['staff'])
def re_stock_product(request, pk):
    product = Product.objects.get(id=pk)

    amt = request.POST['productavailable']
    amt = int(amt)

    if amt > 0:
        product.amt_available = amt
        product.verified = True
        product.published = True
        product.restocking = False
        product.re_evaluating = False
        product.available = True
        product.save()
        messages.info(request, "Product stock verified and product re-published.")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        messages.info(request, "Only quantities above 0 are valid.")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))



@allowed_users(allowed_roles=['staff'])
def view_images(request, pk):
    template = 'adminverify/product_images.html'

    product = Product.objects.get(pk=pk)
    images = product.productimages_set.all()

    if request.method == "POST":
        imageform = ImageUpload(request.POST, request.FILES)
    else:
        imageform = ImageUpload()

    context = {'productimages': images, "chgform":imageform}
    return render(request, template, context)


@allowed_users(allowed_roles=['staff'])
def delete_product_image(request, pk):
    image = ProductImages.objects.get(pk=pk)

    image.delete()

    messages.info(request, "image successfully deleted.")
    return redirect('adminverify')


@allowed_users(allowed_roles=['staff'])
def change_product_image(request, pk):
    image_obj = ProductImages.objects.get(pk=pk)

    if request.method == "POST":
        imageform = ImageUpload(request.POST, request.FILES)

        if imageform.is_valid():
            image = request.FILES.get('image')
            image_obj.image = image
            image_obj.save()

            messages.info(request, "image successfully changed.")
    else:
        imageform = ImageUpload(request.POST, request.FILES)

    return redirect('adminverify')

@allowed_users(allowed_roles=['staff'])
def paid(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    #if product.paid == True
    product.paid = True
    product.save()
    paid = messages.info(request, 'Product payment has been verified.')

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@allowed_users(allowed_roles=['staff'])
def unpay(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    #if product.paid == True
    product.paid = False
    product.save()
    paid = messages.info(request, 'Product payment has been reverted.')

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@allowed_users(allowed_roles=['staff'])
def verify(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    if product.paid == True:
        product.verified = True
        product.save()
        verified = messages.info(request, 'Product has been verified.')
    else:
        unverified = messages.info(request, 'Product verification failed, payment must be received first.')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@allowed_users(allowed_roles=['staff'])
def unverify(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    if product.verified == True:
        product.verified = False
        product.save()
        verified = messages.info(request, 'Product has been unverified.')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@allowed_users(allowed_roles=['staff'])
def product_update(request, pk): #new products

    product = get_object_or_404(Product, pk=pk)
    unverified = Product.objects.all().filter(published=False).order_by('-req_date')
    customer = product.product_seller
    profile = get_object_or_404(Profile, customer=customer)

    if request.method == "POST":
        imageform = ImageUpload(request.POST, request.FILES)

        if imageform.is_valid():
            try:
                image = request.FILES['image']
            except:
                image = product.image

        name = request.POST['productname']
        details = request.POST['productdetails']
        price = request.POST['productprice']
        category = request.POST['productcategory']
        condition = request.POST['productcondition']
        amt = request.POST['productavailable']

        product.image = image
        product.name = name
        product.details = details
        product.price = price
        product.category = category[2:4]
        product.condition = condition[2:4]
        product.pub_date = datetime.datetime.now()
        product.amt_available = amt
        product.edited = False
        product.published = True
        product.save()

        details = "Hey %s! your product '%s' has just been published, head over to ChegBase and check it out." %(customer.user.username, product.name)
        email = EmailMessage(
                "Product published",
                details,
                settings.EMAIL_HOST_USER,
                [profile.email],
        )
        email.fail_silently = True
        email.send()


    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@allowed_users(allowed_roles=['staff'])
def product_update_evaluate(request, pk): #products that have been edited or restocked

    product, created = Product.objects.get_or_create(pk=pk)
    unverified = Product.objects.all().filter(published=False, edited=True, re_evaluating=True).order_by('-req_date')
    customer = product.product_seller
    profile = get_object_or_404(Profile, customer=customer)

    if request.method == "POST":
        imageform = ImageUpload(request.POST, request.FILES)

        if imageform.is_valid():
            try:
                image = request.FILES['image']
            except:
                image = product.image

        name = request.POST['productname']
        details = request.POST['productdetails']
        price = request.POST['productprice']
        category = request.POST['productcategory']
        condition = request.POST['productcondition']
        amt = request.POST['productavailable']

        product.image = image
        product.name = name
        product.details = details
        product.price = price
        product.category = category[2:4]
        product.condition = condition[2:4]
        product.amt_available = amt
        product.edited = False
        product.re_evaluating = False
        product.published = True
        product.save()

        details = "Hey %s! your product '%s' has just been re-published, head over to ChegBase and check it out." %(customer.user.username, product.name)
        email = EmailMessage(
                "Product re-published",
                details,
                settings.EMAIL_HOST_USER,
                [profile.email],
        )
        email.fail_silently = True
        email.send()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
