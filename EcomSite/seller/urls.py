from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller, name='sellerhome'),
    path('register/', views.registerseller, name='registerseller'),
    path('product/', views.create_product, name='createproduct'),
]
