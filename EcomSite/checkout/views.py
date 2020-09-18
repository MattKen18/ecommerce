from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShippingForm
from .decorators import has_shipping
from store.models import Address, Cart, OrderItem, SingleBuy, Customer, Order, SoldItem
from store.decorators import authenticated_user, unauthenticated_user
from django.http import JsonResponse, HttpResponse
import json

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

@authenticated_user
def delete_cart_item(request, pk, mode):
    template = 'store/checkout.html'

    if mode == 'cart':
        cart = get_object_or_404(Cart, user=request.user)
        order_item = get_object_or_404(OrderItem, id=pk, cart=cart)

        order_item.delete()
        messages.info(request, "Item removed from cart")
    elif mode == 'single':
        order_item = get_object_or_404(SingleBuy, id=pk)

        order_item.delete()
        messages.info(request, "Item removed from cart")

    return redirect('checkout')


@authenticated_user
def checkout_quantity_change(request, pk, mode):
    template = 'store/cart.html'
    no_more_stock = ''
    order_quantity = request.POST.get('item_quantity')
    if order_quantity == '':
        order_quantity = 0
    else:
        order_quantity = int(order_quantity)
    #product = get_object_or_404(Product, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if mode == "cart":
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

    elif mode == "single":
        order_item, created = SingleBuy.objects.get_or_create(id=pk)#, product=product)

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


    return redirect('checkout')


@authenticated_user
@has_shipping
def checkout(request):
    template = 'checkout/checkout.html'

    customer = get_object_or_404(Customer, user=request.user)#Customer.objects.get(user=request.user)
    address = get_object_or_404(Address, user=request.user)#Address.objects.get(user=request.user)
    singles = SingleBuy.objects.filter(customer=customer)

    if singles.exists():

        #checks if the product stock of a single buy item has been decreased and if its
        #less than the item quantity then it pegs it to the remaining product amt_available
        #and eventually reloads the page
        reload = False
        for item in singles:
            item_product = item.product
            product_amt = item_product.amt_available
            if item.quantity > product_amt:
                reload = True #as long as there is a item that has too much quantity then it has to reload
                item.quantity = product_amt
                item.save()
                messages.info(request, "%s's stock has been decreased to %s" %(item.product.name, item.quantity))

        total = 0
        for item in singles:
            total += float(item.total())

        if reload == True:
            return redirect('checkout')

        context = {"address": address, "single": singles, "cart_total": total}
    else:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = OrderItem.objects.filter(cart=cart)

        reload = False
        for item in cart_items:
            item_product = item.product
            product_amt = item_product.amt_available
            if item.quantity > product_amt:
                reload = True #as long as there is a item that has too much quantity then it has to reload
                item.quantity = product_amt
                item.save()
                messages.info(request, "%s's stock has been decreased to %s" %(item.product.name, item.quantity))

        total = 0
        for item in cart_items:
            total += float(item.total())

        if reload == True:
            return redirect('checkout')

        context = {"address": address, "order_items": cart_items, "cart_total": total}

    return render(request, template, context)



@authenticated_user
def paymentComplete(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    customer = get_object_or_404(Customer, user=user)
    singles = SingleBuy.objects.filter(customer=customer)

    #make ordered = True on the order_item objects

    if singles.exists():
        order = Order.objects.create(user=user)
        for item in singles:
            item_product = item.product
            total = item_product.amt_sold + item_product.amt_available
            item_product.amt_sold += item.quantity
            item_product.save()
            item_product.amt_available = total - item_product.amt_sold
            if item_product.amt_available <= 0:
                item_product.available = False #restock
            item_product.save()
            SoldItem.objects.create(seller=item.product.product_seller, name=item.product.name,
                                    details=item.product.details, price=item.product.price,
                                    quantity=item.quantity, products_left=item_product.amt_available,
                                    image=item.product.image)
            order.singleitems.add(item)
            order.sellers.add(item.product.product_seller) #added afterwards
            sellers = [item.product.product_seller for item in order.singleitems.all()]
            prices = [item.total() for item in order.singleitems.all()]
            order_details = list(zip(sellers, prices))
            seller_emails = [item.product.product_seller.user.email for item in order.singleitems.all()]
            #print(order_details)
            send_mail(
                "You've got an Order!",
                'Hey %s! You just got an order from %s for \'%s\'.' %(item.product.product_seller, user, item.product.name),
                'djangoecom808@gmail.com',
                ['djangoecom808@gmail.com', '{}'.format(item.product.product_seller.user.email) ],
                fail_silently=False,
            )
            item.delete()


    else:
        cart_items = OrderItem.objects.filter(cart=cart)
        order = Order.objects.create(user=user)
        for item in cart_items:
            item_product = item.product
            total = item_product.amt_sold + item_product.amt_available
            item_product.amt_sold += item.quantity
            item_product.save()
            item_product.amt_available = total - item_product.amt_sold
            if item_product.amt_available <= 0:
                item_product.available = False #restock
            item_product.save()
            SoldItem.objects.create(seller=item.product.product_seller, name=item.product.name,
                                    details=item.product.details, price=item.product.price,
                                    quantity=item.quantity, products_left=item_product.amt_available,
                                    image=item.product.image)
            order.items.add(item)
            order.sellers.add(item.product.product_seller)
            sellers = [item.product.product_seller for item in order.items.all()]
            prices = [item.total() for item in order.items.all()]
            order_details = list(zip(sellers, prices))
            seller_emails = [item.product.product_seller.user.email for item in order.items.all()]
            #print(order_details)
            send_mail(
                "You've got an Order!",
                'Hey %s! You just got an order from %s for your product %s.' %(item.product.product_seller, user, item.product.name),
                'djangoecom808@gmail.com',
                ['djangoecom808@gmail.com', '{}'.format(item.product.product_seller.user.email) ],
                fail_silently=False,
            )
            item.delete()

    #body = json.loads(request.body)
    #print("BODY:", body)
    messages.info(request, "Items successfully purchased")
    return redirect("checkout")
