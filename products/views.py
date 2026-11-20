from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, Category, Brand, Review, ProductShade


def product_list_view(request):
    """Product Listing / Shop page with extensive filters and sorting"""
    products = Product.objects.all().select_related('category', 'brand')

    # Search keyword
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category', '').strip()
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Brand filter
    brand_slug = request.GET.get('brand', '').strip()
    selected_brand = None
    if brand_slug:
        selected_brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=selected_brand)

    # Min / Max price filter
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except Exception:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except Exception:
            pass

    # Rating filter
    rating_filter = request.GET.get('rating', '').strip()
    if rating_filter:
        try:
            products = products.filter(rating__gte=Decimal(rating_filter))
        except Exception:
            pass

    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating', '-review_count')
    elif sort == 'popularity':
        products = products.order_by('-review_count', '-rating')
    elif sort == 'new':
        products = products.order_by('-created_at')
    elif sort == 'bestseller':
        products = products.order_by('-is_bestseller', '-rating')
    else:
        # Default featured
        products = products.order_by('-is_featured', '-created_at')

    # Total count before pagination
    total_count = products.count()

    # Pagination: 9 products per page
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'total_count': total_count,
        'query': query,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'category_slug': category_slug,
        'brand_slug': brand_slug,
        'min_price': min_price,
        'max_price': max_price,
        'rating_filter': rating_filter,
        'sort': sort,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'products/product_list.html', context)


def category_products_view(request, category_slug):
    """Direct category filter shortcut"""
    category = get_object_or_404(Category, slug=category_slug)
    # Redirect with clean URL param
    return redirect(f"/shop/?category={category.slug}")


def product_detail_view(request, slug):
    """Product Details Page with images, shade swatches, reviews, and related products"""
    product = get_object_or_404(Product.objects.select_related('category', 'brand'), slug=slug)
    shades = product.shades.all()
    additional_images = product.additional_images.all()
    reviews = product.reviews.all()

    # Calculate review distribution
    review_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in reviews:
        if r.rating in review_counts:
            review_counts[r.rating] += 1
    total_rev = reviews.count() or 1
    review_percent = {k: int(round((v / total_rev) * 100)) for k, v in review_counts.items()}

    # Related products from same category
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'shades': shades,
        'additional_images': additional_images,
        'reviews': reviews,
        'review_percent': review_percent,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def submit_review_view(request, slug):
    """Submit a verified review for a product"""
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        author_name = request.POST.get('author_name', '').strip()
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '').strip()
        comment = request.POST.get('comment', '').strip()

        if not author_name and request.user.is_authenticated:
            author_name = request.user.get_full_name() or request.user.username
        elif not author_name:
            author_name = "Glam Connoisseur"

        if comment:
            Review.objects.create(
                product=product,
                user=request.user if request.user.is_authenticated else None,
                author_name=author_name,
                rating=rating,
                title=title or "Pure Luxury",
                comment=comment,
                verified=True
            )
            # Update product rating and review count
            all_revs = product.reviews.all()
            total_revs = all_revs.count()
            avg_rating = sum(r.rating for r in all_revs) / total_revs
            product.review_count = total_revs
            product.rating = Decimal(str(round(avg_rating, 1)))
            product.save()

            messages.success(request, "✨ Your glowing review has been published! Thank you for sharing your experience.")
        else:
            messages.error(request, "Please enter your review comment before submitting.")

    return redirect('product_detail', slug=slug)


def quick_view_api(request, product_id):
    """JSON API for quick view modal"""
    product = get_object_or_404(Product.objects.select_related('brand', 'category'), id=product_id)
    shades_data = [
        {'id': s.id, 'name': s.name, 'color_hex': s.color_hex, 'in_stock': s.in_stock}
        for s in product.shades.all()
    ]
    images_data = [product.main_image]
    if product.hover_image and product.hover_image != product.main_image:
        images_data.append(product.hover_image)
    for img in product.additional_images.all():
        if img.image_url not in images_data:
            images_data.append(img.image_url)

    data = {
        'id': product.id,
        'title': product.title,
        'slug': product.slug,
        'url': f"/product/{product.slug}/",
        'brand': product.brand.name if product.brand else "GLOW & GLAM",
        'category': product.category.name,
        'price': f"${product.price:.2f}",
        'original_price': f"${product.original_price:.2f}" if product.original_price else None,
        'discount_percent': product.discount_percent,
        'rating': float(product.rating),
        'review_count': product.review_count,
        'short_description': product.short_description,
        'description': product.description,
        'stock': product.stock,
        'in_stock': product.in_stock,
        'badge_text': product.badge_text,
        'images': images_data,
        'shades': shades_data,
    }
    return JsonResponse(data)


def search_autocomplete_api(request):
    """JSON API for search autocomplete in navigation bar"""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(title__icontains=query) |
        Q(category__name__icontains=query) |
        Q(brand__name__icontains=query)
    )[:6]

    results = []
    for p in products:
        results.append({
            'title': p.title,
            'url': f"/product/{p.slug}/",
            'image': p.main_image,
            'price': f"${p.price:.2f}",
            'category': p.category.name,
        })
    return JsonResponse({'results': results})
