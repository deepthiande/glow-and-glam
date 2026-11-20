# ✨ GLOW & GLAM - Luxury Beauty & Cosmetics E-Commerce Platform

A modern, attractive, fully responsive **Makeup and Beauty Products E-Commerce Website** built with **Python Django**, **HTML5**, **CSS3**, and **Vanilla JavaScript** (No React / frontend frameworks).

Designed with a high-end luxury beauty aesthetic inspired by Sephora, Charlotte Tilbury, and Glossier.

---

## 🎨 Theme & Color Palette
- **Brand Name**: GLOW & GLAM (Haute Beauty • Paris • New York)
- **Palette**: Soft pink (`#FDF2F4`, `#FCE7EC`), Nude & Beige (`#FBF8F5`, `#F5EBE1`), White (`#FFFFFF`), Rose Gold (`#B76E79`, `#C88A83`), and Charcoal/Espresso accents (`#2C2224`).
- **Typography**: `Cormorant Garamond` (editorial serif headings) & `Outfit` (clean sans-serif body).
- **Animations**: Subtle image zoom, hover flip transitions, floating badges, slide-down search, animated toast alerts, and modal dialogs.
- **Responsiveness**: Mobile, tablet, and desktop optimized with sticky navigation and mobile drawer.

---

## 🌟 Key Features & Requirements Matrix

| Section | Features Included |
|---|---|
| **1. Theme & Design** | Soft pink, nude, rose gold, white palette; rounded luxury cards, smooth transitions. |
| **2. Home Page** | Hero banner ("Beauty Begins With You", "Discover your beauty. Express your style.", Shop Now CTA), trust badges (Cruelty Free, Clean Beauty), 10 category cards with images, featured products, best sellers, special 20% discount promo banner, customer reviews, newsletter subscription. |
| **3. Sticky Navigation** | Brand logo, Home, Shop All, Categories mega-dropdown, Best Sellers, About Us, Contact, live search with autocomplete, wishlist badge, cart bag badge, user profile menu. |
| **4. 10 Product Categories** | Lipsticks, Foundations, Concealers, Blush, Highlighters, Eyeshadows, Eyeliners, Mascaras, Makeup Brushes, Skincare. Each with high-res photography and clickable navigation. |
| **5. Product Listing / Shop** | Responsive grid, product cards with main & hover image, brand name, star ratings, price & discount badge, shade dots, Quick View modal, AJAX Add to Cart, Wishlist heart toggle, filters for category, brand, price range, ratings, and multi-option sorting. |
| **6. Product Details Page** | Multi-image gallery with clickable thumbnails, shade swatches selector, quantity stepper, Add to Cart, 1-Click Buy Now, guarantee accords, customer reviews summary & breakdown, review submission form, and related products. |
| **7. Shopping Cart** | Add/remove items, quantity increase/decrease with real-time AJAX recalculation, free shipping progress bar ($50 threshold), coupon discount system (`GLAM20`, `GLOW10`, `FREESHIP`), tax calculation, grand total. |
| **8. User Authentication** | User registration, user login (supports email/username), forgot password flow, profile management, and comprehensive order history with status tracking. |
| **9. Checkout Page** | Customer contact, delivery address, shipping method (Standard vs Express Glam), payment methods (Credit/Debit Card demo form, UPI, Cash on Delivery), order notes, and order placement saving to database. |
| **10. Order Confirmation** | Unique order number (e.g. `GG-XXXXXXXX`), order tracking timeline, itemized receipt breakdown, delivery address, and print/continue shopping options. |
| **11. About Us & Contact** | Brand story, clean beauty philosophy, cruelty-free commitment, working contact inquiry form, flagship boutique address, helpline, email, social links, and FAQ accordion. |
| **12. Footer** | Brand tagline, quick links, customer care, newsletter signup, accepted payment badges, social media links, and copyright. |

---

## 🚀 Quick Start Guide

### 1. Run the Development Server
```bash
python manage.py runserver
```
Visit the website in your browser at:  
👉 **http://127.0.0.1:8000/**

---

## 🔑 Demo Accounts & Test Credentials

### Demo Customer
- **Username**: `sophia`
- **Password**: `glam123`
*(Pre-loaded with sample profile details, address, and past order history!)*

### Administrator / Superuser
- **Username**: `admin`
- **Password**: `admin123`
*(Access Django admin at: **http://127.0.0.1:8000/admin/**)*

---

## 🎟️ Active Promotional Coupon Codes
Apply these promo codes in the Shopping Bag (`/cart/`):
- **`GLAM20`** — **20% OFF** your entire order (Featured on the top announcement bar and promo banner)
- **`GLOW10`** — **10% OFF** your entire order
- **`BEAUTY15`** — **15% OFF** orders over $40
- **`FREESHIP`** — Complimentary shipping on orders over $20

---

## 🧪 Automated Integration Tests
Run the comprehensive test suite verifying all 18 core routes and user journeys:
```bash
python test_app.py
```
Outputs:
```text
✅ Home Page: 200 OK
✅ Shop Page: 200 OK
✅ Category Filter (Lipsticks): 200 OK
✅ Product Search: 200 OK
✅ Product Detail Page: 200 OK
✅ Quick View JSON API: 200 OK
✅ Search Autocomplete API: 200 OK
✅ AJAX Add to Cart: 200 OK
✅ Shopping Cart View: 200 OK
✅ Coupon System (GLAM20): 200 OK
✅ Wishlist Toggle: 200 OK
✅ Wishlist View: 200 OK
✅ Checkout Page: 200 OK
✅ Order Placement & DB Creation: 200 OK
✅ Order Confirmation & Receipt View: 200 OK
✅ About Us Page: 200 OK
✅ Contact Us Page & Working Contact Form: 200 OK
✅ User Authentication, Profile & Past Order History: 200 OK
🎉 ALL 18 CORE INTEGRATION TESTS PASSED PERFECTLY! 🎉
```

---

## 📂 Project Architecture

```
make/
├── manage.py
├── seed_data.py               # Seeds categories, products, shades, reviews, demo users
├── test_app.py                # Full integration test suite
├── db.sqlite3                 # Pre-populated SQLite database
├── glowglam_project/          # Django core settings and URL routing
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                      # Home, About, Contact, Newsletter
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── products/                  # Catalog, 10 categories, reviews, quick view API
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── cart/                      # Cart, CartItem, Wishlist, Coupon, context processors
│   ├── models.py
│   ├── views.py
│   ├── context_processors.py
│   └── urls.py
├── orders/                    # Order, OrderItem, Checkout, Confirmation, Tracking
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── accounts/                  # User profile, login, registration, order history
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── static/
│   ├── css/
│   │   └── style.css          # Luxury responsive styling, variables, keyframes
│   └── js/
│       └── main.js            # Vanilla JS: AJAX cart/wishlist, quick view, gallery
└── templates/
    ├── base.html              # Sticky navigation, announcement bar, toasts, footer
    ├── core/
    │   ├── home.html          # Hero, 10 categories, featured, promo banner, reviews
    │   ├── about.html         # Brand story, clean beauty values
    │   └── contact.html       # Working contact form, FAQs
    ├── products/
    │   ├── product_list.html  # Filters, sorting, search, pagination
    │   ├── product_detail.html# Gallery, shade swatches, review form, related items
    │   └── includes/
    │       └── product_card.html # Reusable card component
    ├── cart/
    │   ├── cart.html          # Quantity update, coupons, shipping progress bar
    │   └── wishlist.html      # Saved items with Move-to-Bag
    ├── orders/
    │   ├── checkout.html      # Shipping address, card/UPI/COD demo payment
    │   ├── order_confirmation.html # Order receipt & tracking timeline
    │   └── order_detail.html  # Order view
    └── accounts/
        ├── login.html
        ├── register.html
        ├── profile.html       # Profile edit & past order history
        └── forgot_password.html
```
