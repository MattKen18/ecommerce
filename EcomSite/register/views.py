from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group
# Create your views here.
from store.decorators import authenticated_user, unauthenticated_user

@unauthenticated_user
def register_user(response):#this is the same as sign up
    if response.method == "POST":
        regform = RegisterForm(response.POST)

        if regform.is_valid:
            user = regform.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            return redirect("login")

    else:
        regform = RegisterForm()

    context = {"regform": regform}

    return render(response, "register/register.html", context)

@authenticated_user
def logout(request):
    context = {}
    template = 'registration/logout.html'

    return render(request, template, context)


#def shipping(request):
#    template = 'register/shipping.html'
#    context = {}
#    return render(request, template, context)
