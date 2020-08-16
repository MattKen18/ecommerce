import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from store.models import Product, categories, conditions
from .forms import ImageUpload
# Create your views here.

def admin_verify(request):
    template = 'adminverify/admin_verify.html'
    unverified = Product.objects.all().filter(published=False).order_by('-req_date')
    categories = Product._meta.get_field('category').choices
    conditions = Product._meta.get_field('condition').choices

    if request.method == "POST":
        imageform = ImageUpload(request.POST)
    else:
        imageform = ImageUpload()

    context = {'products': unverified, 'categories': categories, 'conditions': conditions, 'imageform': imageform}
    return render(request, template, context)

def paid(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    #if product.paid == True
    product.paid = True
    product.save()
    paid = messages.info(request, 'Product payment has been verified.')
    return redirect('adminverify')


def verify(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    if product.paid == True:
        product.verified = True
        product.save()
        verified = messages.info(request, 'Product has been verified.')
    else:
        unverified = messages.info(request, 'Product verification failed, payment must be received first.')
    return redirect('adminverify')

def unverify(request, pk):
    product, created = Product.objects.get_or_create(pk=pk)
    if product.verified == True:
        product.verified = False
        product.save()
        verified = messages.info(request, 'Product has been unverified.')
    return redirect('adminverify')

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

    return redirect('adminverify')
