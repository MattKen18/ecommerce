from django.shortcuts import render
from .forms import SellerForm

# Create your views here.

def seller(request):
    template = 'seller/home.html'
    context = {}



    return render(request, template, context)


def registerseller(request):
    template = 'seller/register.html'
    if request.method == "POST":
        sellerform = SellerForm(request.POST)


    else:
        sellerform = SellerForm()
    context = {"sellerform": sellerform}



    return render(request, template, context)
