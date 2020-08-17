from django.urls import path
from . import views

urlpatterns = [
        path('', views.admin_verify, name="adminverify"),
        path('update/<uuid:pk>', views.product_update, name="productupdate"),
        path('paid/<uuid:pk>', views.paid, name="paid"),
        path('verify/<uuid:pk>', views.verify, name="verify"),
        path('unverify/<uuid:pk>', views.unverify, name="unverify"),
        path('unverifiedimages/<uuid:pk>', views.view_images, name="viewimages"),
        path('unverifiedimages/delete/<int:pk>/', views.delete_product_image, name="deleteproductimage"),
        path('unverifiedimages/change/<int:pk>/', views.change_product_image, name="changeproductimage"),

]
