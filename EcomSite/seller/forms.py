from django import forms
from store.models import Customer
from django.contrib.auth.models import User
from .models import *

class SellerForm(forms.Form):
    #home address
    address_line1 = forms.CharField(max_length=200)
    address_line2 = forms.CharField(max_length=200)
    state = forms.CharField(max_length=200)
    zip_code = forms.CharField(max_length=200)
    country = forms.CharField(max_length=200)

    class Meta:
        model = HomeAddress
        fields = ['address_line1', 'address_line2', 'state', 'zip_code', 'country']


    #identification
    #trn_number = forms.CharField(max_length=200)
