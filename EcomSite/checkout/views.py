from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShippingForm
from .decorators import has_shipping
from store.models import Address, Cart, OrderItem, SingleBuy, Customer, Order, SoldItem
from seller.models import Profile
from store.decorators import authenticated_user, unauthenticated_user
from django.http import JsonResponse, HttpResponse
import json

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

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
        for item in singles:
            if item.product.published == True:
                pass
            else:
                item.delete()
                messages.info(request, """An item has been removed from your cart,
                                        this may be due to the product being altered
                                        by product seller.""")
                return redirect("checkout")
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
        empty = False

        for item in cart_items:
            if item.product.published == True:
                pass
            else:
                item.delete()
                messages.info(request, """An item has been removed from your cart,
                                        this may be due to the product being altered
                                        by product seller.""")
                return redirect("checkout")

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

        if cart_items.count() == 0:
            empty = True

        context = {"address": address, "order_items": cart_items, "cart_total": total, "empty": empty}

    return render(request, template, context)


def send_order_notice(seller, user, item): #send email to seller of each cart item that was bought
    template = render_to_string('checkout/order_notice_template.html', {'name': seller.user.username,
                                                                 'buyer': user, 'item': item})
    email = EmailMessage(
            "You've got an Order!",
            template,
            settings.EMAIL_HOST_USER,
            [seller.email],
    )
    email.fail_silently = True
    email.send()

def send_order_details_notice(buyer, order, tranID): #send email to buyer
    template = render_to_string('checkout/order_details_template.html', {'buyer': buyer, 'order': order,
                                                                         'tranID': tranID})
    email = EmailMessage(
            "Order details",
            template,
            settings.EMAIL_HOST_USER,
            [buyer.email],
    )
    email.fail_silently = True
    email.send()

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

            seller_profiles = []
            for cus in sellers:
                seller_profiles.append(Profile.objects.get(user=cus.user))

            prices = [item.total() for item in order.singleitems.all()]
            order_details = list(zip(sellers, prices))
            seller_emails = [item.product.product_seller.user.email for item in order.singleitems.all()]

            for seller in seller_profiles: #sends email to all the sellers
                send_order_notice(seller, user, item)

        singleitems_order = order.singleitems.all()
        send_order_details_notice(user, singleitems_order, order.id) #sends email to customer/buyer

        for item in singles:
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

            seller_profiles = []
            for cus in sellers:
                seller_profiles.append(Profile.objects.get(user=cus.user))

            prices = [item.total() for item in order.items.all()]
            order_details = list(zip(sellers, prices))
            seller_emails = [item.product.product_seller.user.email for item in order.items.all()]

            for seller in seller_profiles: #sends email to all the sellers
                send_order_notice(seller, user, item)

        cartitems_order = order.items.all()
        send_order_details_notice(user, cartitems_order, order.id) #sends email to customer/buyer

        for item in cart_items:
            item.delete()

    return JsonResponse("Payment Complete!", safe=False)
    #body = json.loads(request.body)
    #print("BODY:", body)
