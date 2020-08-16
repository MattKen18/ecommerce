from django import forms
from store.models import Product

class ImageUpload(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['image']
