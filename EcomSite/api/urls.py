from django.urls import path
from . import views

urlpatterns = [
    path('product-list/', views.productList, name='apiproductlist'),
    path('product-detail/<uuid:pk>', views.productDetail, name='apiproductdetail'),

]
