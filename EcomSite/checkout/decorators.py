from django.http import HttpResponse
from django.shortcuts import redirect
from store.models import Address
from django.contrib import messages

def has_shipping(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            shipping = Address.objects.get(user=request.user)
        except:
            messages.info(request, "We don't have a shipping address for you, please give us one below.")
            return redirect('shipping')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
