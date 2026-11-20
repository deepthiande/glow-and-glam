from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_view, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/apply-coupon/', views.apply_coupon_view, name='apply_coupon'),
    path('cart/remove-coupon/', views.remove_coupon_view, name='remove_coupon'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist_view, name='toggle_wishlist'),
    path('wishlist/move-to-cart/<int:item_id>/', views.move_to_cart_view, name='move_to_cart'),
]
