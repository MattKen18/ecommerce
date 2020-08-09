from django.shortcuts import render

# Create your views here.

def sellerprofile(request):
    template = 'sellerprofile/profile.html'
    context = {}

    return render(request, template, context)
