from django import forms
from django.contrib.auth.models import User
from store.models import Address

class ShippingForm(forms.Form):
    address_line1 = forms.CharField(max_length=200)
    address_line2 = forms.CharField(max_length=200)
    state = forms.CharField(max_length=200)
    zip_code = forms.CharField(max_length=200)
    country = forms.CharField(max_length=200)

    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'state', 'zip_code', 'country']
