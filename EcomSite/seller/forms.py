from django import forms
from store.models import Customer, Product, conditions, categories
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.forms import UserCreationForm

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



class UserForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    username = forms.CharField(max_length=30, required=False)



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

        labels = {"email": "Business email"}



class MiscForm(forms.ModelForm):
    class Meta:# add business help text
        model = Profile
        fields = ['note']
        widgets = {'note': forms.Textarea(attrs={"placeholder":"This is the perfect time to lay out your terms...",
                                                 "style": "resize: none;"})}
        labels = {"note": "Seller's Note"}



class ProPicForm(forms.ModelForm):
    profile_pic = forms.ImageField(label="Select a profile picture")
    class Meta:
        model = Profile
        fields = ['profile_pic']


class CreateProductForm(forms.ModelForm):
    price = forms.FloatField(min_value=1)
    #details = forms.CharField(max_length=150, help_text="e.g. The Hate You Give hardcover by Angie Thomas 2 years old. ")
    category = forms.ChoiceField(choices=categories)
    image = forms.ImageField(required=False)
    condition = forms.ChoiceField(choices=conditions)
    amt_available = forms.IntegerField(min_value=1)

    class Meta:
        model = Product
        fields = ['name', 'price', 'details', 'category', 'image', 'condition', 'amt_available']
        widgets = {'details': forms.Textarea(attrs={"style": "resize: none;", "rows": 5})}
        labels = {"name": "Title"}

class AddPrimaryImage(forms.Form):
    primaryimage = forms.ImageField(required=True)


class AddSecondaryImages(forms.ModelForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = ProductImages
        fields = ['image']

class EditProduct(forms.ModelForm):
    name = forms.CharField(required=False, max_length=50, label="Title")
    price = forms.FloatField(required=False, min_value=1)
    details = forms.CharField(required=False, max_length=150, help_text="e.g. The Hate You Give hardcover by Angie Thomas 2 years old. ")
    category = forms.ChoiceField(required=False, choices=categories)
    image = forms.ImageField(required=False)
    condition = forms.ChoiceField(required=False, choices=conditions)
    class Meta:
        model = Product
        fields = [ 'image', 'name', 'price', 'details', 'category', 'condition']


class Restock(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['amt_available']
        labels = {'amt_available': 'Restock To'}
