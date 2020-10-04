from django import forms
from .models import *
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import UserCreationForm

class CustomerInfoform(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', "email"]

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CustomerInfoform, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        for field, value in self.fields.items():
            self.fields[field].required = False


class CustomerUserform(forms.ModelForm):
    username = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ["username"]

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CustomerUserform, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        for field, value in self.fields.items():
            self.fields[field].required = False

class CustomerPasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["password1", "password2"]


class CustomerShippingAddressForm(forms.ModelForm):
    #shipping address
    address_line1 = forms.CharField(max_length=200, required=False, label="Address line 1 (Street)")
    address_line2 = forms.CharField(max_length=200, required=False, label="Address line 2 (Post-Office)")
    city = forms.CharField(max_length=200, required=False, label="Town/City")
    state = forms.CharField(max_length=200, required=False, label="State/Parish/Province")
    zip_code = forms.CharField(max_length=200, required=False, label="Zip Code")

    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country',]
        widgets = {'country': CountrySelectWidget()}
