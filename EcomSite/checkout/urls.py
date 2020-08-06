from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name="checkout"),
    path('shipping/', views.shipping, name="shipping"),
    #path('update-shipping/', views.create_shipping_info, name="updateshipping"),

]
