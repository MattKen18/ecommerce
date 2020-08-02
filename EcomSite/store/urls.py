from django.urls import path
from . import views

urlpatterns = [
        path('', views.store, name = 'store'),
        path('signup/', views.signup, name='signup'),
        path('add_to_cart/<int:pk>', views.add_to_cart, name='addtocart'),
        path('cart/', views.cart, name="cart"),
        path('checkout/', views.checkout, name = 'checkout'),
]
