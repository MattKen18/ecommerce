from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from store.models import Customer, Product
from .models import Profile

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

def is_seller(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            customer = Customer.objects.get(user=request.user)
        except:
            return redirect('register')
        else:
            if customer.seller == True:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('registerseller')

    return wrapper_func

def profile_exists(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            return redirect('registerseller')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
