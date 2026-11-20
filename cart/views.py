from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from products.models import Product, ProductShade
from .models import Cart, CartItem, Coupon, WishlistItem


def _get_or_create_cart(request):
    """Retrieve or create the active shopping cart for authenticated user or guest session"""
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        # Check if user has an existing cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        # If there's an orphaned guest cart from this session, merge its items
        if session_key:
            guest_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
            if guest_cart and guest_cart != cart:
                for item in guest_cart.items.all():
                    existing = cart.items.filter(product=item.product, shade=item.shade).first()
                    if existing:
                        existing.quantity += item.quantity
                        existing.save()
                    else:
                        item.cart = cart
                        item.save()
                if guest_cart.coupon and not cart.coupon:
                    cart.coupon = guest_cart.coupon
                    cart.save()
                guest_cart.delete()
        return cart
    else:
        cart, created = Cart.objects.get_or_create(session_key=session_key, user__isnull=True)
        return cart


def _get_wishlist_query(request):
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        return WishlistItem.objects.filter(user=request.user)
    elif session_key:
        return WishlistItem.objects.filter(session_key=session_key)
    return WishlistItem.objects.none()


def cart_view(request):
    """Main Shopping Cart Page"""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.select_related('product', 'shade', 'product__category')

    # Calculate free shipping progress bar ($50 threshold)
    threshold = Decimal('50.00')
    subtotal = cart.subtotal
    remaining_for_free_ship = max(Decimal('0.00'), threshold - subtotal)
    shipping_progress = min(100, int((subtotal / threshold) * 100)) if threshold > 0 else 100

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'remaining_for_free_ship': remaining_for_free_ship,
        'shipping_progress': shipping_progress,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart_view(request):
    """Add product with optional shade and quantity to cart"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        shade_id = request.POST.get('shade_id')
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

        product = get_object_or_404(Product, id=product_id)
        shade = None
        if shade_id:
            try:
                shade = ProductShade.objects.get(id=shade_id, product=product)
            except ProductShade.DoesNotExist:
                shade = None
        elif product.shades.exists():
            # Default to first shade if available and not selected
            shade = product.shades.first()

        cart = _get_or_create_cart(request)

        # Check if item with this product & shade already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            shade=shade,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # If "buy_now" was clicked, redirect straight to checkout!
        is_buy_now = request.POST.get('buy_now') == '1'
        if is_buy_now:
            return redirect('checkout')

        success_msg = f"✨ Added {quantity}x '{product.title}' to your luxury shopping bag!"

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': success_msg,
                'cart_items_count': cart.total_items,
                'cart_subtotal': f"${cart.subtotal:.2f}",
                'grand_total': f"${cart.grand_total:.2f}",
            })

        messages.success(request, success_msg)
        return redirect(request.META.get('HTTP_REFERER', 'cart'))

    return redirect('shop')


def update_cart_view(request, item_id):
    """Update quantity of an item in the cart"""
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        action = request.POST.get('action') # 'increase', 'decrease', or 'set'
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif action == 'set':
            try:
                qty = int(request.POST.get('quantity', 1))
                if qty > 0:
                    cart_item.quantity = qty
                    cart_item.save()
                else:
                    cart_item.delete()
            except (ValueError, TypeError):
                pass

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            item_exists = CartItem.objects.filter(id=item_id).exists()
            return JsonResponse({
                'status': 'success',
                'item_exists': item_exists,
                'item_quantity': cart_item.quantity if item_exists else 0,
                'item_total': f"${cart_item.total_price:.2f}" if item_exists else "$0.00",
                'cart_items_count': cart.total_items,
                'subtotal': f"${cart.subtotal:.2f}",
                'discount': f"${cart.discount_total:.2f}",
                'shipping': f"${cart.shipping_fee:.2f}",
                'tax': f"${cart.tax_amount:.2f}",
                'grand_total': f"${cart.grand_total:.2f}",
            })

    return redirect('cart')


def remove_from_cart_view(request, item_id):
    """Remove an item from cart"""
    cart = _get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_title = cart_item.product.title
    cart_item.delete()

    success_msg = f"Removed '{product_title}' from your shopping bag."
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': success_msg,
            'cart_items_count': cart.total_items,
            'subtotal': f"${cart.subtotal:.2f}",
            'discount': f"${cart.discount_total:.2f}",
            'shipping': f"${cart.shipping_fee:.2f}",
            'tax': f"${cart.tax_amount:.2f}",
            'grand_total': f"${cart.grand_total:.2f}",
        })

    messages.info(request, success_msg)
    return redirect('cart')


def apply_coupon_view(request):
    """Apply promotional coupon code"""
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip().upper()
        cart = _get_or_create_cart(request)

        if not code:
            messages.error(request, "Please enter a valid coupon code.")
            return redirect('cart')

        try:
            coupon = Coupon.objects.get(code=code, active=True)
            if cart.subtotal < coupon.min_order_amount:
                messages.error(request, f"Coupon '{code}' requires a minimum order of ${coupon.min_order_amount:.2f}.")
            else:
                cart.coupon = coupon
                cart.save()
                messages.success(request, f"✨ Glamorous! Coupon '{code}' applied successfully. You saved ${cart.discount_total:.2f}!")
        except Coupon.DoesNotExist:
            messages.error(request, f"Coupon code '{code}' is invalid or expired. Try using GLAM20 for 20% off!")

    return redirect('cart')


def remove_coupon_view(request):
    """Remove active coupon from cart"""
    cart = _get_or_create_cart(request)
    cart.coupon = None
    cart.save()
    messages.info(request, "Coupon removed from your bag.")
    return redirect('cart')


def wishlist_view(request):
    """Wishlist Page"""
    items = _get_wishlist_query(request).select_related('product', 'product__category', 'product__brand')
    return render(request, 'cart/wishlist.html', {'wishlist_items': items})


def toggle_wishlist_view(request, product_id):
    """Toggle a product in wishlist (Add/Remove)"""
    product = get_object_or_404(Product, id=product_id)
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    # Find existing
    if request.user.is_authenticated:
        item = WishlistItem.objects.filter(user=request.user, product=product).first()
        if item:
            item.delete()
            action = 'removed'
            msg = f"'{product.title}' removed from your wishlist."
        else:
            WishlistItem.objects.create(user=request.user, product=product)
            action = 'added'
            msg = f"✨ '{product.title}' added to your wishlist!"
        count = WishlistItem.objects.filter(user=request.user).count()
    else:
        item = WishlistItem.objects.filter(session_key=session_key, product=product).first()
        if item:
            item.delete()
            action = 'removed'
            msg = f"'{product.title}' removed from your wishlist."
        else:
            WishlistItem.objects.create(session_key=session_key, product=product)
            action = 'added'
            msg = f"✨ '{product.title}' added to your wishlist!"
        count = WishlistItem.objects.filter(session_key=session_key).count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'action': action,
            'message': msg,
            'wishlist_count': count,
        })

    if action == 'added':
        messages.success(request, msg)
    else:
        messages.info(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))


def move_to_cart_view(request, item_id):
    """Move an item from wishlist to cart"""
    if request.user.is_authenticated:
        wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    else:
        wishlist_item = get_object_or_404(WishlistItem, id=item_id, session_key=request.session.session_key)

    product = wishlist_item.product
    cart = _get_or_create_cart(request)
    first_shade = product.shades.first()

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        shade=first_shade,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    wishlist_item.delete()
    messages.success(request, f"✨ Moved '{product.title}' to your luxury shopping bag!")
    return redirect('cart')
