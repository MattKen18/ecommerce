from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer

from store.models import Product
# Create your views here.

@api_view(['GET']) #only allows a get path
def productList(request): #gets list of all products
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET']) #only allows a get path
def productDetail(request, pk): #gets a specific product
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)
