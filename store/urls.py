from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_list/', views.order_list, name='order_list'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('verify_payment/<int:order_id>/', views.verify_payment, name='verify_payment'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
]
