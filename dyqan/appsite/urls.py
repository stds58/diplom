from django.urls import path
from .views import (ProductList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete, \
   OrderList, OrderDetail, OrderCreate, OrderUpdate, OrderDelete, \
   CategoryList, CategoryDetail, CategoryCreate, CategoryUpdate, CategoryDelete, \
   CountryList, CountryDetail, CountryCreate, CountryUpdate, CountryDelete, \
   ImageList, add_in_basket, delete_from_basket, OrderProductDetail)


urlpatterns = [

   path('products/', ProductList.as_view(), name= 'products'),
   path('products/<int:pk>/', ProductDetail.as_view(), name= 'product'),
   path('products/create/', ProductCreate.as_view(), name='product_create'),
   path('products/<int:pk>/edit/', ProductUpdate.as_view(), name='product_update'),
   path('products/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),

   path('orders/', OrderList.as_view(), name= 'orders'),
   path('orders/<int:pk>/', OrderDetail.as_view(), name= 'order'),
   path('orders/create/', OrderCreate.as_view(), name='order_create'),
   path('orders/<int:pk>/edit/', OrderUpdate.as_view(), name='order_update'),
   path('orders/<int:pk>/delete/', OrderDelete.as_view(), name='order_delete'),

   path('categorys/', CategoryList.as_view(), name= 'categorys'),
   path('categorys/<int:pk>/', CategoryDetail.as_view(), name='category'),
   path('categorys/create/', CategoryCreate.as_view(), name='category_create'),
   path('categorys/<int:pk>/edit/', CategoryUpdate.as_view(), name='category_update'),
   path('categorys/<int:pk>/delete/', CategoryDelete.as_view(), name='category_delete'),

   path('countrys/', CountryList.as_view(), name='countrys'),
   path('countrys/<int:pk>/', CountryDetail.as_view(), name='country'),
   path('countrys/create/', CountryCreate.as_view(), name='country_create'),
   path('countrys/<int:pk>/edit/', CountryUpdate.as_view(), name='country_update'),
   path('countrys/<int:pk>/delete/', CountryDelete.as_view(), name='country_delete'),

   path('images/', ImageList.as_view(), name= 'imgs'),

   path('products/<int:pk>/add_in_basket/', add_in_basket, name='add_in_basket'),
   path('products/<int:pk>/delete_from_basket/', delete_from_basket, name='delete_from_basket'),
   path('orderproducts/<int:pk>/', OrderProductDetail.as_view(), name= 'orderproduct'),

]
