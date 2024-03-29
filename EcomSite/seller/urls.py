from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.seller, name='sellerhome'),
    path('register/', views.registerseller, name='registerseller'),
    path('register/profile_image/', views.upload_profilepic, name='profilepic'),
    path('product/', views.create_product, name='createproduct'),
    path('deleteproduct/<uuid:pk>', views.delete_product, name='deleteproduct'),
    path('paid/', views.seller_paid, name='paid'),
    path('addimages/<uuid:pk>/<str:mode>/create/', views.add_images, name='addimages'),
    path('addimages/<uuid:pk>/<str:mode>/modify/', views.add_images_after, name='addimagesafter'),
    path('deleteimage/<int:pk>/', views.delete_image, name='deleteimage'),
    path('payment/<uuid:pk>/', views.product_payment, name='productpayment'),
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
    path('user/profile/<int:pk>/<str:username>/', views.profileview, name='profileview'),
    path('user/userprofile/<int:pk>/<str:username>/', views.personalprofileview, name='personalprofileview'),
    path('user/profile/<int:pk>/<str:username>/products/', views.profile_seller_products, name='sellerproductsview'),

]
