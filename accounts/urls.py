from django.urls import path
from .views import *
urlpatterns = [
   path('',home,name='home'),
   path('products/',products,name='products'),
   path('customer/<int:customer_id>/',customer,name='customer'),
   path('update_order/<int:order_id>/',update_order,name='update_order'),
   path('delete_order/<int:order_id>/',delete_order,name='delete_order'),
   path('create_order/<int:customer_id>/', create_order, name='create_order'),

]
