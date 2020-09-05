from django import forms
from django.contrib.auth.models import User
from store.models import Address
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class ShippingForm(forms.ModelForm):
    address_line1 = forms.CharField(max_length=200, label="Address line 1 (Street)")
    address_line2 = forms.CharField(max_length=200,  label="Address line 2 (Post-Office)")
    state = forms.CharField(max_length=200, label="State/Parish/Province")
    city = forms.CharField(max_length=200, label="Town/City")
    zip_code = forms.CharField(max_length=200, required=False, label="Zip Code")

    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country']
        widgets = {'country': CountrySelectWidget()}


    # to add form control to all fields    
	#def __init__(self, *args, **kwargs):
	#	super(ContactForm, self).__init__(*args, **kwargs)
	#	for field in self.fields:
	#		self.fields[field].widget.attrs.update({
	#	    'class': 'form-control'})
