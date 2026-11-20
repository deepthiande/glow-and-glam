from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation_view, name='order_confirmation'),
    path('order/<str:order_number>/', views.order_detail_view, name='order_detail'),
]
