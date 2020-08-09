from django.urls import path
from . import views

urlpatterns = [
    path('', views.sellerprofile, name='profile')
]
