from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name="checkout"),
    path('shipping/', views.shipping, name="shipping"),
    path('paymentcomplete/', views.paymentComplete, name="complete"),
    path('delete_item/<uuid:pk>/<str:mode>/', views.delete_cart_item, name='deletecartitem'),
    path('checkout/change_quantity/<uuid:pk>/<str:mode>/', views.checkout_quantity_change, name='checkoutchangeqty'),
    #path('update-shipping/', views.create_shipping_info, name="updateshipping"),

]
