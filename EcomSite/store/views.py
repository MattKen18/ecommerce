from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# Create your views here.

def store(response):  #order by
    #option to request order of book
    template = 'store/store.html'
    products = Product.objects.all().filter(published=True, rejected=False).order_by('-pub_date')
    choices = Product._meta.get_field('category').choices
    categories = [choice[1] for choice in choices]

    paginator = Paginator(products, 20)

    page_number = response.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {"products": products, "categories": categories, 'page_obj': page_obj}

    return render(response, template, context)


def store_categories(response, category):  #order by
    if category == 'textbook' or category == 'TB':
        template = 'store/store_textbooks.html'
        products = Product.objects.filter(category='TB').order_by('-pub_date')

    elif category == 'notebook' or category == 'NB' :
        template = 'store/store_notebooks.html'
        products = Product.objects.filter(category='NB').order_by('-pub_date')

    elif category == 'reading book' or category == 'RB':
        template = 'store/store_reading.html'
        products = Product.objects.filter(category='RB').order_by('-pub_date')

    elif category == 'literature book' or category == 'LB':
        template = 'store/store_literature.html'
        products = Product.objects.filter(category='LB').order_by('-pub_date')

    choices = Product._meta.get_field('category').choices
    categories = [choice[1] for choice in choices]

    paginator = Paginator(products, 20)

    page_number = response.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {"products": products, "categories": categories, 'page_obj': page_obj}

    return render(response, template, context)


def detail_page(request, pk):
    template = "store/detail.html"
    product, created = Product.objects.get_or_create(id=pk)


    context = {'product': product}

    return render(request, template, context)


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    order_item, created = OrderItem.objects.get_or_create(cart=cart, product=product)

    try:
        detail_amt = request.POST['detailorder_amt']

    except:
        if order_item.quantity < order_item.product.amt_available:
            order_item.quantity += 1
            order_item.save()
        else:
            no_more_stock = messages.error(request, 'No more items in stock, currently there are ' + str(order_item.product.amt_available) + ' item(s) available.')

    else:
        detail_amt = int(detail_amt)
        if order_item.quantity + detail_amt <= order_item.product.amt_available:
            order_item.quantity += detail_amt
            order_item.save()
        else:
            no_more_stock = messages.error(request, 'No more items in stock, currently there are ' + str(order_item.product.amt_available) + ' item(s) available.')


    return redirect('cart')


def single_buy(request, pk):
    product = get_object_or_404(Product, pk=pk)
    customer = get_object_or_404(Customer, user=request.user)
    single_buy, created = SingleBuy.objects.get_or_create(customer=customer, product=product)
    no_more_stock = ''

    try:
        detail_single_amt = request.POST['detailorder_amt']
        detail_single_amt = int(detail_single_amt)

    except:
        if single_buy.quantity >= single_buy.product.amt_available:
            no_more_stock = messages.error(request, 'No more items in stock, currently there are ' + str(single_buy.product.amt_available) + ' item(s) available.')
            return redirect('store')
        else:
            single_buy.quantity += 1
            single_buy.save()

    else:
        if single_buy.quantity >= single_buy.product.amt_available or single_buy.quantity + detail_single_amt > single_buy.product.amt_available:
            no_more_stock = messages.error(request, 'No more items in stock, currently there are ' + str(single_buy.product.amt_available) + ' item(s) available.')
            return redirect('detail', pk=pk)
        else:
            single_buy.quantity = detail_single_amt
            single_buy.save()

    return redirect('shipping')



def del_single_buy(request):
    customer = get_object_or_404(Customer, user=request.user)
    singles = SingleBuy.objects.filter(customer=customer).delete()

    return redirect("checkout")

def cart(request):
    template = 'store/cart.html'
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = OrderItem.objects.filter(cart=cart)

    total_items = cart_items.count()

    total_price = 0
    for item in cart_items:
        total_price += item.total()


    context = {"cart": cart_items, "items":total_items, "total":total_price}

    return render(request, template, context)


def quantity_change(request, pk):
    template = 'store/cart.html'
    no_more_stock = ''
    order_quantity = request.POST.get('item_quantity')
    if order_quantity == '':
        order_quantity = 0
    else:
        order_quantity = int(order_quantity)
    #product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    order_item, created = OrderItem.objects.get_or_create(id=pk, cart=cart)#, product=product)

    if order_quantity > order_item.product.amt_available:
        order_item.quantity = order_item.product.amt_available
        order_item.save()
        no_more_stock = messages.error(request, 'No more items in stock, currently there are '
                        + str(order_item.product.amt_available) + ' item(s) available.')
    elif order_quantity <= order_item.product.amt_available and order_quantity > 0:
        order_item.quantity = 0
        order_item.quantity = order_quantity
        order_item.save()

    elif order_quantity == 0:
        order_item.delete()


    return redirect('cart')

def delete_item(request, pk):
    template = 'store/cart.html'
    deleted = ''

    cart, created = Cart.objects.get_or_create(user=request.user)
    order_item, created = OrderItem.objects.get_or_create(id=pk, cart=cart)#, product=product)

    order_item.delete()
    deleted = messages.info(request, "Item removed from cart")
    return redirect('cart')

def login(request):
    context = {}
    template = 'store/login.html'

    return render(request, template, context)


def signup(request):
    context = {}
    template = 'store/signup.html'
    #Customer()

    return render(request, template, context)



#response.user to get the current user details
