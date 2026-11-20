from products.models import Category
from .models import Cart, WishlistItem


def glow_glam_context(request):
    """Provides cart, wishlist, and category data to all templates."""
    # Ensure session key exists for guest users
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    # Retrieve or create cart
    cart = None
    cart_items_count = 0
    cart_subtotal = 0

    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        elif session_key:
            cart = Cart.objects.filter(session_key=session_key).first()

        if cart:
            cart_items_count = cart.total_items
            cart_subtotal = cart.subtotal
    except Exception:
        pass

    # Retrieve wishlist
    wishlist_count = 0
    wishlist_product_ids = set()
    try:
        if request.user.is_authenticated:
            wishlist_items = WishlistItem.objects.filter(user=request.user)
        elif session_key:
            wishlist_items = WishlistItem.objects.filter(session_key=session_key)
        else:
            wishlist_items = []

        wishlist_count = wishlist_items.count() if hasattr(wishlist_items, 'count') else len(wishlist_items)
        wishlist_product_ids = set(wishlist_items.values_list('product_id', flat=True)) if hasattr(wishlist_items, 'values_list') else set()
    except Exception:
        pass

    # Categories for navigation
    categories = Category.objects.all()[:12]

    return {
        'cart': cart,
        'cart_items_count': cart_items_count,
        'cart_subtotal': cart_subtotal,
        'wishlist_count': wishlist_count,
        'wishlist_product_ids': wishlist_product_ids,
        'nav_categories': categories,
    }
