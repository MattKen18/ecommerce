from django import forms
from store.models import Customer, Product, conditions, categories
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import *
from store.models import ProductImages



class AddressForm(forms.ModelForm):
    #home address
    address_line1 = forms.CharField(max_length=200, required=False, label="Address line 1 (Street)")
    address_line2 = forms.CharField(max_length=200, required=False, label="Address line 2 (Post-Office)")
    city = forms.CharField(max_length=200, required=False, label="Town/City")
    state = forms.CharField(max_length=200, required=False, label="State/Parish/Province")
    zip_code = forms.CharField(max_length=200, required=False, label="Zip Code")

    class Meta:
        model = HomeAddress
        fields = ['address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country',]
        widgets = {'country': CountrySelectWidget()}

class DateInput(forms.DateInput):
    input_type = 'date'


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'gender']
        widgets = {'date_of_birth': DateInput()}

class ContactForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['email', 'phone']
        widgets = {'email': forms.EmailInput()}


class MiscForm(forms.ModelForm):
    class Meta:# add business help text
        model = Profile
        fields = ['business']


class ProPicForm(forms.ModelForm):
    profile_pic = forms.ImageField(label="Select a profile picture")
    class Meta:
        model = Profile
        fields = ['profile_pic']


class CreateProductForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label="Title")
    price = forms.FloatField(min_value=1)
    details = forms.CharField(max_length=200, help_text="e.g. The Hate You Give hardcover by Angie Thomas 2 years old. ")
    category = forms.ChoiceField(choices=categories)
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    condition = forms.ChoiceField(choices=conditions)
    amt_available = forms.IntegerField(min_value=1)

    class Meta:
        model = Product
        fields = ['name', 'price', 'details', 'category', 'image', 'condition', 'amt_available']

class AddSecondaryImages(forms.ModelForm):
    image = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ProductImages
        fields = ['image']

class EditProduct(forms.ModelForm):
    name = forms.CharField(required=False, max_length=200, label="Title")
    price = forms.FloatField(required=False, min_value=1)
    details = forms.CharField(required=False, max_length=200, help_text="e.g. The Hate You Give hardcover by Angie Thomas 2 years old. ")
    category = forms.ChoiceField(required=False, choices=categories)
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    condition = forms.ChoiceField(required=False, choices=conditions)
    amt_available = forms.IntegerField(required=False, min_value=1)
    class Meta:
        model = Product
        fields = [ 'image', 'name', 'price', 'details', 'category', 'condition', 'amt_available']
