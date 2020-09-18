from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.seller, name='sellerhome'),
    path('register/', views.registerseller, name='registerseller'),
    path('register/profile_image/', views.upload_profilepic, name='profilepic'),
    path('product/', views.create_product, name='createproduct'),
    path('deleteproduct/<uuid:pk>', views.delete_product, name='deleteproduct'),
    path('paid/', views.seller_paid, name='paid'),
    path('addimages/', views.add_images, name='addimages'),
    path('userprofile/', views.seller_profile, name='profile'),
    path('userprofile/update/<str:form>/', views.update_seller_profile, name='updateprofile'),
    path('sellerproducts/', views.seller_products, name='sellerproducts'),
    path('restockproducts/', views.restock, name='restockproducts'), #shows all products
    path('restockproducts/<uuid:pk>', views.restock_product, name='restockproduct'), #request restock by seller for individual product
    path('requestpickup/', views.request_pickup, name='pickup'),
    path('makepickup/', views.pickup, name='makepickup'),
    path('sales/', views.seller_sales, name='sales'),
    path('paymentinquiries/', views.payment_inquiries, name='inquiries'),
    path('editproduct/<uuid:pk>/', views.editproduct, name='editproduct'),
    path('vouch/<uuid:pk>/', views.vouch, name='vouch'),

]
