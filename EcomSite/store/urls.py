from django.urls import path
from . import views

urlpatterns = [
        path('', views.store, name = 'store'),
        path('store/<str:category>/', views.store_categories, name='categories'),
        path('add_to_cart/<uuid:pk>/', views.add_to_cart, name='addtocart'),
        path('singlebuy/<uuid:pk>/', views.single_buy, name='single'),
        path('del_singlebuy/', views.del_single_buy, name='delsingle'),
        path('cart/', views.cart, name="cart"),
        path('cart/clear_cart/', views.clear_cart, name='clearcart'),
        path('cart/change_quantity/<uuid:pk>/', views.quantity_change, name='changeqty'),
        path('cart/delete_item/<uuid:pk>/', views.delete_item, name='deleteitem'),
        path('product-detail/<uuid:pk>/', views.detail_page, name='detail'),
        path('search_results/', views.search_results, name='searchresults'),
        path('Account/<str:username>/<str:form>/', views.account_settings, name='accountsettings'),

]

#path('notebooks/', views.store_notebooks, name = 'notebook'),
#path('literature/', views.store_literature, name = 'literature book'),
#path('reading/', views.store_readings, name = 'reading book'),
