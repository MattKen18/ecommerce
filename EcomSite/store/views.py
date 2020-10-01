from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from seller.models import Profile, HomeAddress
from .models import *
from checkout.decorators import has_shipping
from .decorators import authenticated_user, unauthenticated_user, allowed_users
# Create your views here.

def store(response):  #order by
    #option to request order of book
    template = 'store/store.html'
    products = Product.objects.all().filter(paid=True, verified=True, published=True,
                                            rejected=False, available=True,
                                            amt_available__gt=0).order_by('-pub_date')
    choices = Product._meta.get_field('category').choices
    categories = [choice[1] for choice in choices]
    sellers = Profile.objects.all().filter(tier="T3").order_by('-tier_points')[:10]

    paginator = Paginator(products, 20)

    page_number = response.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {"products": products, "categories": categories, 'page_obj': page_obj, 'sellers': sellers}

    return render(response, template, context)


def store_categories(response, category):  #order by
    sellers = Profile.objects.all().filter(tier="T3").order_by('-tier_points')[:10]

    if category == 'Textbooks' or category == 'TB':
        template = 'store/store_textbooks.html'
        products = Product.objects.filter(published=True, rejected=False, category='TB').order_by('-pub_date')

    elif category == 'Notebooks' or category == 'NB' :
        template = 'store/store_notebooks.html'
        products = Product.objects.filter(published=True, rejected=False, category='NB').order_by('-pub_date')

    elif category == 'Reading Books' or category == 'RB':
        template = 'store/store_reading.html'
        products = Product.objects.filter(published=True, rejected=False, category='RB').order_by('-pub_date')

    elif category == 'Literature Books' or category == 'LB':
        template = 'store/store_literature.html'
        products = Product.objects.filter(published=True, rejected=False, category='LB').order_by('-pub_date')

    choices = Product._meta.get_field('category').choices
    categories = [choice[1] for choice in choices]

    paginator = Paginator(products, 20)

    page_number = response.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {"products": products, "categories": categories, 'page_obj': page_obj, 'sellers': sellers}

    return render(response, template, context)


def detail_page(request, pk):
    template = "store/detail.html"
    user = request.user
    product = get_object_or_404(Product, id=pk)
    customerSeller = product.product_seller.user
    images = product.productimages_set.all()
    customer = get_object_or_404(Customer, user=customerSeller) #seller of the current product in the detail page i.e the customer whose user field is the seller of the product
    seller_products = Product.objects.all().filter(product_seller=product.product_seller,
                                                   published=True).exclude(id=product.id).order_by("-pub_date")[:12]
    #this 'block' is to get the order item of the product that the user has in his/her cart, this is to get the amt that the user has in his/her cart
    #to show in the detail page
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
        order_items = OrderItem.objects.filter(product=product)
        detail_product = None #this will be the specific order_item
        for item in order_items:
            if item.cart == cart:
                detail_product = item
    else:
        detail_product = None

    seller = get_object_or_404(Profile, user=customerSeller)
    seller_orders = SoldItem.objects.filter(seller=customer).count() #all the completed orders for the products of this seller
    homeaddress = get_object_or_404(HomeAddress, profile=seller)#check if home address will be automatically created if not made from seller sign up

    #for image in images:
    #    print(image.imageURL)

    context = {'product': product, 'productimages': images, "seller": seller,
               "homeaddress": homeaddress, "sellerorders": seller_orders,
               'detailproduct': detail_product, "seller_products": seller_products}

    return render(request, template, context)

def search_results(response):
    template = "store/search_results.html"
    search_query = response.GET['searchprompt'].strip()
    if search_query == '':
        return redirect('store')
    else:
        products = Product.objects.all()
        filtered_products = products.filter(name__icontains=search_query,
                                            available=True, published=True,
                                            restocking=False, verified=True,
                                            paid=True)
        paginator = Paginator(filtered_products, 5)

        page_number = response.GET.get('page')

        page_obj = paginator.get_page(page_number)



        context = {"results": filtered_products, "prompt": search_query, 'page_obj': page_obj,}

    return render(response, template, context)


@authenticated_user
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    order_item, created = OrderItem.objects.get_or_create(cart=cart, product=product)

    if product.paid == False or product.verified == False or product.published == False:
        messages.info(request, "Product has not been published.")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        try:
            detail_amt = request.POST['detailorder_amt'] #adding to cart from the detail page

        except: # adding to cart from store
            if order_item.quantity < order_item.product.amt_available:
                order_item.quantity += 1
                order_item.save()
                added_to_cart = messages.error(request, 'Item added to cart')
            elif order_item.quantity <= 0: #if adding item that has no stock, then prevent it from showing in cart i.e deleting it
                order_item.delete()
            elif order_item.quantity == order_item.product.amt_available:
                no_more_stock = messages.error(request, 'No more items in stock, currently there are ' + str(order_item.product.amt_available) + ' item(s) available.')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            else:
                no_more_stock = messages.error(request, 'No more items in stock, currently there are ' + str(order_item.product.amt_available) + ' item(s) available.')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

        else:
            detail_amt = int(detail_amt)
            if detail_amt != 0:
                if order_item.quantity + detail_amt <= order_item.product.amt_available:
                    order_item.quantity += detail_amt
                    order_item.save()
                    added_to_cart = messages.error(request, 'Item added to cart')
                else:
                    if order_item.quantity <= 0:
                        order_item.delete()
                    no_more_stock = messages.error(request, 'No more items in stock, currently there are ' + str(order_item.product.amt_available) + ' item(s) available.')
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            else:
                if order_item.quantity >= 1:
                    add_more = messages.error(request, 'Quantity should be at least 1.')
                else:
                    order_item.delete()
                    add_more = messages.error(request, 'Quantity should be at least 1.')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect('cart')

@authenticated_user
@has_shipping
def single_buy(request, pk):
    product = get_object_or_404(Product, pk=pk)
    customer = get_object_or_404(Customer, user=request.user)
    single_buy, created = SingleBuy.objects.get_or_create(customer=customer, product=product)
    no_more_stock = ''
    
    if product.paid == False or product.verified == False or product.published == False:
        messages.info(request, "Product has not been published.")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        try:
            detail_single_amt = request.POST['detailorder_amt']
            detail_single_amt = int(detail_single_amt)

        except:
            if single_buy.quantity >= single_buy.product.amt_available:
                single_buy.delete()
                no_more_stock = messages.error(request, 'No more items in stock, currently there are ' + str(single_buy.product.amt_available) + ' item(s) available.')
                return redirect('store')
            else:
                single_buy.quantity += 1
                single_buy.save()

        else:
            if single_buy.quantity >= single_buy.product.amt_available or single_buy.quantity + detail_single_amt > single_buy.product.amt_available:
                single_buy.delete()
                no_more_stock = messages.error(request, 'No more items in stock, currently there are ' + str(single_buy.product.amt_available) + ' item(s) available.')
                return redirect('detail', pk=pk)
            else:
                single_buy.quantity = detail_single_amt
                single_buy.save()

    return redirect('checkout')


@authenticated_user
def del_single_buy(request):
    customer = get_object_or_404(Customer, user=request.user)
    singles = SingleBuy.objects.filter(customer=customer).delete()

    return redirect("checkout")


@authenticated_user
def cart(request):
    template = 'store/cart.html'
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = OrderItem.objects.filter(cart=cart)

    for item in cart_items:
        if item.product.published == True:
            pass
        else:
            item.delete()
            messages.info(request, """An item has been removed from your cart,
                                    this may be due to the product being altered
                                    by product seller.""")
            return redirect("cart")


    total_items = cart_items.count()

    total_price = 0
    for item in cart_items:
        total_price += item.total()


    context = {"cart": cart_items, "items": total_items, "total": total_price}

    return render(request, template, context)


@authenticated_user
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

@authenticated_user
def delete_item(request, pk):
    template = 'store/cart.html'
    deleted = ''

    cart, created = Cart.objects.get_or_create(user=request.user)
    order_item, created = OrderItem.objects.get_or_create(id=pk, cart=cart)#, product=product)

    order_item.delete()
    deleted = messages.info(request, "Item removed from cart")
    return redirect('cart')




#def login(request):
#    context = {}
#    template = 'store/login.html'

#    return render(request, template, context)


#def signup(request):
#    context = {}
#    template = 'store/signup.html'
#    #Customer()
#
#    return render(request, template, context)



#response.user to get the current user details
