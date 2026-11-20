from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from products.models import Product, ProductShade


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(default=0, help_text="Percentage discount, e.g. 20 for 20%")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Fixed amount discount if percent is 0")
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}% off)" if self.discount_percent else f"{self.code} (${self.discount_amount} off)"

    def calculate_discount(self, subtotal):
        if subtotal < self.min_order_amount:
            return Decimal('0.00')
        if self.discount_percent > 0:
            return (subtotal * Decimal(self.discount_percent) / Decimal(100)).quantize(Decimal('0.01'))
        elif self.discount_amount > 0:
            return min(subtotal, self.discount_amount)
        return Decimal('0.00')


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='carts', null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} - {'User: ' + self.user.username if self.user else 'Guest: ' + str(self.session_key)}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def discount_total(self):
        if self.coupon and self.items.exists():
            return self.coupon.calculate_discount(self.subtotal)
        return Decimal('0.00')

    @property
    def shipping_fee(self):
        if not self.items.exists():
            return Decimal('0.00')
        # Free shipping over $50
        return Decimal('0.00') if self.subtotal >= Decimal('50.00') else Decimal('5.00')

    @property
    def tax_amount(self):
        if not self.items.exists():
            return Decimal('0.00')
        # 5% luxury cosmetic tax / sales tax
        taxable = max(Decimal('0.00'), self.subtotal - self.discount_total)
        return (taxable * Decimal('0.05')).quantize(Decimal('0.01'))

    @property
    def grand_total(self):
        if not self.items.exists():
            return Decimal('0.00')
        total = self.subtotal - self.discount_total + self.shipping_fee + self.tax_amount
        return max(Decimal('0.00'), total).quantize(Decimal('0.01'))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shade = models.ForeignKey(ProductShade, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['id']

    def __str__(self):
        shade_str = f" ({self.shade.name})" if self.shade else ""
        return f"{self.quantity}x {self.product.title}{shade_str}"

    @property
    def unit_price(self):
        return self.product.price

    @property
    def total_price(self):
        return (self.product.price * self.quantity).quantize(Decimal('0.01'))


class WishlistItem(models.Model):
    user = models.ForeignKey(User, related_name='wishlist_items', null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Wishlist: {self.product.title}"
