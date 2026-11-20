from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductShade, Review

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductShadeInline(admin.TabularInline):
    model = ProductShade
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_featured']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'brand', 'price', 'original_price', 'stock', 'rating', 'is_featured', 'is_bestseller']
    list_filter = ['category', 'brand', 'is_featured', 'is_bestseller', 'is_new_arrival']
    search_fields = ['title', 'description', 'brand__name']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductShadeInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'product', 'rating', 'created_at', 'verified']
    list_filter = ['rating', 'verified', 'created_at']
    search_fields = ['author_name', 'title', 'comment', 'product__title']
