from django.http import HttpResponse
from django.shortcuts import redirect
from store.models import Customer

def not_seller(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            customer = Customer.objects.get(user=request.user)
        except:
            return redirect('register')
        else:
            if customer.seller == False:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('sellerhome')

    return wrapper_func
