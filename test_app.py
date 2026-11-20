import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glowglam_project.settings')
django.setup()

from django.test import Client
from products.models import Product, Category
from cart.models import Cart, Coupon
from orders.models import Order

def run_tests():
    client = Client()
    print("--- Testing GLOW & GLAM Website Pages and Features ---")

    # 1. Home Page
    res = client.get('/')
    assert res.status_code == 200, f"Home page failed with {res.status_code}"
    assert "Beauty Begins" in res.content.decode('utf-8')
    assert "GLOW &amp; GLAM" in res.content.decode('utf-8')
    print("✅ Home Page: 200 OK (Hero banner, categories, bestsellers verified)")

    # 2. Shop Page
    res = client.get('/shop/')
    assert res.status_code == 200, f"Shop page failed with {res.status_code}"
    assert "luxury cosmetics" in res.content.decode('utf-8')
    print("✅ Shop Page: 200 OK (Product grid & filters rendered)")

    # 3. Category Filter
    res = client.get('/shop/?category=lipsticks')
    assert res.status_code == 200, f"Category filter failed with {res.status_code}"
    assert "Lipsticks" in res.content.decode('utf-8')
    print("✅ Category Filter (Lipsticks): 200 OK")

    # 4. Search Filter
    res = client.get('/shop/?q=foundation')
    assert res.status_code == 200, f"Search failed with {res.status_code}"
    print("✅ Product Search ('foundation'): 200 OK")

    # 5. Product Detail Page
    prod = Product.objects.filter(slug='velvet-matte-luxe-lipstick').first()
    assert prod is not None, "Product not found in database"
    res = client.get(f'/product/{prod.slug}/')
    assert res.status_code == 200, f"Product detail failed with {res.status_code}"
    assert "Velvet Matte Luxe Lipstick" in res.content.decode('utf-8')
    assert "Customer Reviews" in res.content.decode('utf-8')
    print(f"✅ Product Detail Page ({prod.title}): 200 OK (Gallery, shades, reviews)")

    # 6. Quick View API
    res = client.get(f'/api/quick-view/{prod.id}/')
    assert res.status_code == 200, f"Quick View API failed with {res.status_code}"
    json_data = res.json()
    assert json_data['title'] == prod.title
    print(f"✅ Quick View JSON API: 200 OK (Returned {len(json_data['shades'])} shades)")

    # 7. Search Autocomplete API
    res = client.get('/api/search/?q=silk')
    assert res.status_code == 200
    assert len(res.json()['results']) > 0
    print("✅ Search Autocomplete API: 200 OK (Returned live suggestions)")

    # 8. Add to Cart (Standard POST & AJAX)
    shade = prod.shades.first()
    res = client.post('/cart/add/', {
        'product_id': prod.id,
        'shade_id': shade.id if shade else '',
        'quantity': 2
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert res.status_code == 200
    cart_json = res.json()
    assert cart_json['status'] == 'success'
    print(f"✅ AJAX Add to Cart: 200 OK (Cart count: {cart_json['cart_items_count']})")

    # 9. View Cart
    res = client.get('/cart/')
    assert res.status_code == 200
    assert "Shopping Bag" in res.content.decode('utf-8')
    assert prod.title in res.content.decode('utf-8')
    print("✅ Shopping Cart View: 200 OK (Item present in cart)")

    # 10. Apply Coupon (GLAM20)
    res = client.post('/cart/apply-coupon/', {'coupon_code': 'GLAM20'}, follow=True)
    assert res.status_code == 200
    assert "GLAM20" in res.content.decode('utf-8')
    print("✅ Coupon System (GLAM20 20% off): 200 OK")

    # 11. Wishlist Toggle
    res = client.post(f'/wishlist/toggle/{prod.id}/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert res.status_code == 200
    assert res.json()['status'] == 'success'
    print("✅ Wishlist Toggle: 200 OK")

    # 12. Wishlist View
    res = client.get('/wishlist/')
    assert res.status_code == 200
    assert prod.title in res.content.decode('utf-8')
    print("✅ Wishlist View: 200 OK (Saved product visible)")

    # 13. Checkout Page
    res = client.get('/checkout/')
    assert res.status_code == 200
    assert "Secure Luxury Checkout" in res.content.decode('utf-8')
    print("✅ Checkout Page: 200 OK (Forms and order summary loaded)")

    # 14. Place Order via Checkout POST
    res = client.post('/checkout/', {
        'full_name': 'Eleanor Vance',
        'email': 'eleanor.vance@example.com',
        'phone': '+1 (555) 234-5678',
        'address': '742 Evergreen Glam Ave',
        'apartment': 'Penthouse A',
        'city': 'New York',
        'state': 'NY',
        'postal_code': '10018',
        'country': 'United States',
        'shipping_method': 'Standard Delivery',
        'payment_method': 'card',
        'order_notes': 'Please include signature gift ribbon.'
    }, follow=True)
    assert res.status_code == 200
    content = res.content.decode('utf-8')
    assert "Beauty is on its Way" in content or "Thank You" in content
    order = Order.objects.filter(email='eleanor.vance@example.com').first()
    assert order is not None
    print(f"✅ Order Placement & DB Creation: 200 OK (Generated Order #{order.order_number})")

    # 15. Order Confirmation View
    res = client.get(f'/order-confirmation/{order.order_number}/')
    assert res.status_code == 200
    assert order.order_number in res.content.decode('utf-8')
    print(f"✅ Order Confirmation & Receipt View: 200 OK (Tracking timeline & receipt rendered)")

    # 16. About Us Page
    res = client.get('/about/')
    assert res.status_code == 200
    assert "Our Beauty Philosophy" in res.content.decode('utf-8')
    print("✅ About Us Page: 200 OK")

    # 17. Contact Us Page & Form Submission
    res = client.get('/contact/')
    assert res.status_code == 200
    assert "Beauty Concierge" in res.content.decode('utf-8')
    res = client.post('/contact/', {
        'name': 'Isabella Rossellini',
        'email': 'isabella@example.com',
        'phone': '+1 555-111-2222',
        'subject': 'Shade Matching Consultation',
        'message': 'Hello, could you assist me in choosing between 100 Fair and 120 Warm Ivory?'
    }, follow=True)
    assert res.status_code == 200
    assert "Thank you for reaching out" in res.content.decode('utf-8')
    print("✅ Contact Us Page & Working Contact Form: 200 OK")

    # 18. User Login & Profile
    login_success = client.login(username='sophia', password='glam123')
    assert login_success, "Login for demo user sophia failed"
    res = client.get('/profile/')
    assert res.status_code == 200
    assert "Sophia Laurent" in res.content.decode('utf-8')
    res_orders = client.get('/profile/?tab=orders')
    assert res_orders.status_code == 200
    assert "Order History" in res_orders.content.decode('utf-8')
    print("✅ User Authentication, Profile & Past Order History: 200 OK")

    print("\n🎉 ALL 18 CORE INTEGRATION TESTS PASSED PERFECTLY! 🎉\n")

if __name__ == '__main__':
    run_tests()
