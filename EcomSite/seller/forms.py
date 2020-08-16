from django import forms
from store.models import Customer, Product, conditions, categories
from django.contrib.auth.models import User
from .models import *

class AddressForm(forms.Form):
    #home address
    address_line1 = forms.CharField(max_length=200, required=False, label="Address line 1 (Street)")
    address_line2 = forms.CharField(max_length=200, required=False, label="Address line 2 (Post-Office)")
    city = forms.CharField(max_length=200, required=False, label="Town/City")
    state = forms.CharField(max_length=200, required=False, label="State/Parish/Province")
    zip_code = forms.CharField(max_length=200, required=False, label="Zip Code")
    country = forms.CharField(max_length=200, required=False)

    class Meta:
        model = HomeAddress
        fields = ['address_line1', 'address_line2', 'state', 'city', 'zip_code', 'country']


class PersonalForm(forms.Form):
    date_of_birth = forms.DateField()
    gender = forms.ChoiceField(choices=genders)
    citizenship = forms.CharField(max_length=20)

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'gender', 'citizenship']


class CreateProductForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label="Title")
    price = forms.FloatField(min_value=1)
    details = forms.CharField(max_length=200, help_text="e.g. The Hate You Give hardcover by Angie Thomas 2 years old. ")
    category = forms.ChoiceField(choices=categories)
    image = forms.ImageField(required=False)
    condition = forms.ChoiceField(choices=conditions)
    amt_available = forms.IntegerField(min_value=1)

    class Meta:
        model = Product
        fields = ['name', 'price', 'details', 'category', 'image', 'condition', 'amt_available']
