from django.urls import path
from . import views

urlpatterns = [
        path('', views.admin_verify, name="adminverify"),
        path('NewProducts/', views.verify_new, name="verifynew"),
        path('ReEvaluate/', views.re_evaluate, name="reevaluate"),
        path('update/<uuid:pk>', views.product_update, name="productupdate"),
        path('updateEvaluate/<uuid:pk>', views.product_update_evaluate, name="productupdateevaluate"),
        path('paid/<uuid:pk>', views.paid, name="verifypaid"),
        path('unpay/<uuid:pk>', views.unpay, name="verifyunpay"),
        path('verify/<uuid:pk>', views.verify, name="verify"),
        path('unverify/<uuid:pk>', views.unverify, name="unverify"),
        path('unverifiedimages/<uuid:pk>', views.view_images, name="viewimages"),
        path('unverifiedimages/delete/<int:pk>/', views.delete_product_image, name="deleteproductimage"),
        path('unverifiedimages/change/<int:pk>/', views.change_product_image, name="changeproductimage"),

]
