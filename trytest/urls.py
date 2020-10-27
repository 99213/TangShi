from django.urls import path

from . import views
app_name = 'trytest'

urlpatterns = [
    path('', views.index, name='index'),
    path(r'sign/', views.sign, name='sign'),
    path(r'register/', views.register, name='register'),
    path(r'order/', views.order, name='order'),
    path(r'pay/', views.pay, name='pay'),
    path(r'get_order_status/', views.get_order_status, name='get_order_status')
]