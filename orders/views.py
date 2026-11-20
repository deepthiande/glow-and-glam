from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cart.views import _get_or_create_cart
from .models import Order, OrderItem
from .forms import CheckoutForm


def checkout_view(request):
    """Checkout Page with Customer details, shipping address, order summary, and payment"""
    cart = _get_or_create_cart(request)
    if not cart or not cart.items.exists():
        messages.warning(request, "Your luxury shopping bag is currently empty. Please add items before checking out.")
        return redirect('shop')

    cart_items = cart.items.select_related('product', 'shade')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

            # Handle shipping method calculation
            shipping_method = form.cleaned_data.get('shipping_method', 'Standard Delivery')
            if 'Express' in shipping_method:
                shipping_cost = Decimal('15.00')
            else:
                shipping_cost = cart.shipping_fee

            order.shipping_cost = shipping_cost
            order.subtotal = cart.subtotal
            order.discount_amount = cart.discount_total

            taxable = max(Decimal('0.00'), cart.subtotal - cart.discount_total)
            tax_amount = (taxable * Decimal('0.05')).quantize(Decimal('0.01'))
            order.tax_amount = tax_amount

            order.total_price = (cart.subtotal - cart.discount_total + shipping_cost + tax_amount).quantize(Decimal('0.01'))

            # Payment status simulation
            if order.payment_method == 'cod':
                order.payment_status = 'Pending (Cash on Delivery)'
            else:
                order.payment_status = 'Paid (Demo Verified)'

            order.save()

            # Create OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_title=item.product.title,
                    product_image=item.product.main_image,
                    shade_name=item.shade.name if item.shade else "",
                    price=item.product.price,
                    quantity=item.quantity
                )

            # Clear cart
            cart.items.all().delete()
            cart.coupon = None
            cart.save()

            messages.success(request, f"✨ Congratulations! Your order {order.order_number} has been placed successfully.")
            return redirect('order_confirmation', order_number=order.order_number)
        else:
            messages.error(request, "Please verify your shipping details and try again.")
    else:
        # Prepopulate with authenticated user data if available
        initial_data = {
            'shipping_method': 'Standard Delivery',
            'payment_method': 'card',
        }
        if request.user.is_authenticated:
            initial_data['full_name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            initial_data['email'] = request.user.email
            if hasattr(request.user, 'profile'):
                p = request.user.profile
                initial_data['phone'] = p.phone
                initial_data['address'] = p.address
                initial_data['city'] = p.city
                initial_data['state'] = p.state
                initial_data['postal_code'] = p.postal_code
                initial_data['country'] = p.country
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'orders/checkout.html', context)


def order_confirmation_view(request, order_number):
    """Order Success & Receipt Page"""
    order = get_object_or_404(Order.objects.prefetch_related('items'), order_number=order_number)
    return render(request, 'orders/order_confirmation.html', {'order': order})


def order_detail_view(request, order_number):
    """View details of a specific order"""
    order = get_object_or_404(Order.objects.prefetch_related('items'), order_number=order_number)
    # Check permissions if user is authenticated and order belongs to someone else
    if order.user and request.user.is_authenticated and order.user != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('profile')
    return render(request, 'orders/order_detail.html', {'order': order})
