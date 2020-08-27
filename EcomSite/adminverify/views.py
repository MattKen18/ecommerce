import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from store.models import Product, ProductImages, categories, conditions
from .forms import ImageUpload
# Create your views here.

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

def verify_new(request):
    template = "adminverify/newproductsverify.html"
    unverified = Product.objects.all().filter(published=False, re_evaluating=False).order_by('-req_date')
    categories = Product._meta.get_field('category').choices
    conditions = Product._meta.get_field('condition').choices

    if request.method == "POST":
        imageform = ImageUpload(request.POST)
    else:
        imageform = ImageUpload()

    context = {'products': unverified, 'categories': categories, 'conditions': conditions, 'imageform': imageform}
    return render(request, template, context)


def re_evaluate(request):
    template = "adminverify/re_evaluate.html"
    unverified = Product.objects.all().filter(published=False, re_evaluating=True).order_by('-req_date')
    categories = Product._meta.get_field('category').choices
    conditions = Product._meta.get_field('condition').choices

    if request.method == "POST":
        imageform = ImageUpload(request.POST)
    else:
        imageform = ImageUpload()

    context = {'products': unverified, 'categories': categories, 'conditions': conditions, 'imageform': imageform}
    return render(request, template, context)


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


def delete_product_image(request, pk):
    image = ProductImages.objects.get(pk=pk)

    image.delete()

    messages.info(request, "image successfully deleted.")
    return redirect('adminverify')


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


def paid(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    #if product.paid == True
    product.paid = True
    product.save()
    paid = messages.info(request, 'Product payment has been verified.')

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def unpay(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    #if product.paid == True
    product.paid = False
    product.save()
    paid = messages.info(request, 'Product payment has been reverted.')

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def verify(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    if product.paid == True:
        product.verified = True
        product.save()
        verified = messages.info(request, 'Product has been verified.')
    else:
        unverified = messages.info(request, 'Product verification failed, payment must be received first.')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def unverify(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    if product.verified == True:
        product.verified = False
        product.save()
        verified = messages.info(request, 'Product has been unverified.')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def product_update(request, pk):

    product, created = Product.objects.get_or_create(pk=pk)
    unverified = Product.objects.all().filter(published=False).order_by('-req_date')

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
        product.published = True
        product.save()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def product_update_evaluate(request, pk):

    product, created = Product.objects.get_or_create(pk=pk)
    unverified = Product.objects.all().filter(published=False).order_by('-req_date')

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
        product.re_evaluating = False
        product.published = True
        product.save()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
