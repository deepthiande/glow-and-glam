from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.product_list_view, name='shop'),
    path('category/<slug:category_slug>/', views.category_products_view, name='category_products'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('product/<slug:slug>/review/', views.submit_review_view, name='submit_review'),
    path('api/quick-view/<int:product_id>/', views.quick_view_api, name='quick_view_api'),
    path('api/search/', views.search_autocomplete_api, name='search_autocomplete_api'),
]
