from django.urls import path
from . import views

urlpatterns = [
        path('', views.store, name = 'store'),
        path('signup/', views.signup, name='signup'),
        path('add_to_cart/<int:pk>', views.add_to_cart, name='addtocart'),
        path('cart/', views.cart, name="cart"),
        path('cart/decrease_quantity/<int:pk>', views.qty_dec, name='decreaseqty'),
        path('cart/increase_quantity/<int:pk>', views.qty_inc, name='increaseqty'),
]
