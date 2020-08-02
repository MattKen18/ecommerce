from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.

def register_user(response):
    if response.method == "POST":
        regform = RegisterForm(response.POST)

        if regform.is_valid:
            regform.save()

            return redirect("store")

    else:
        regform = RegisterForm()

    context = {"regform": regform}

    return render(response, "register/register.html", context)


def logout(request):
    context = {}
    template = 'registration/logout.html'

    return render(request, template, context)


#def shipping(request):
#    template = 'register/shipping.html'
#    context = {}
#    return render(request, template, context)
