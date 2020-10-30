from django.urls import path

from . import views



app_name = 'trytest'

urlpatterns = [
    path('', views.views.index, name='index'),
    path(r'sign/', views.views.sign, name='sign'),
    path(r'register/', views.views.register, name='register'),
    path(r'order/', views.order.order, name='order'),
    path(r'pay/', views.order.pay, name='pay'),
    path(r'get_order_status/', views.order.get_order_status, name='get_order_status')
]