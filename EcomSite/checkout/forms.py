from django import forms
from django.contrib.auth.models import User
from store.models import Address

class ShippingForm(forms.Form):
    address_line1 = forms.CharField(max_length=200, label="Address line 1 (Street)")
    address_line2 = forms.CharField(max_length=200,  label="Address line 2 (Post-Office)")
    state = forms.CharField(max_length=200, label="State/Parish/Province")
    city = forms.CharField(max_length=200, label="Town/City")
    zip_code = forms.CharField(max_length=200, required=False, label="Zip Code")
    country = forms.CharField(max_length=200)
    
    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country', 'date']
