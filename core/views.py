from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product, Category, Brand
from .models import ContactMessage, NewsletterSubscriber
from .forms import ContactForm, NewsletterForm


def home_view(request):
    """Luxury Home Landing Page"""
    # 1. Featured products
    featured_products = Product.objects.filter(is_featured=True)[:8]

    # 2. Best sellers
    bestsellers = Product.objects.filter(is_bestseller=True)[:8]

    # 3. New arrivals
    new_arrivals = Product.objects.filter(is_new_arrival=True)[:8]

    # 4. Categories with image and product counts
    categories = Category.objects.all()

    # 5. Brands
    brands = Brand.objects.all()

    context = {
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    """About Us page explaining GLOW & GLAM brand philosophy"""
    return render(request, 'core/about.html')


def contact_view(request):
    """Contact page with interactive form, boutique details, and FAQs"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✨ Thank you for reaching out to GLOW & GLAM! Our luxury beauty concierge will respond within 24 hours.")
            return redirect('contact')
        else:
            messages.error(request, "Please check the form fields and submit again.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})


def newsletter_subscribe(request):
    """AJAX or POST newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address.'}, status=400)
            messages.error(request, 'Please provide a valid email address.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
        msg = "✨ Welcome to the GLOW & GLAM VIP Club! Check your inbox for your 20% discount code: GLAM20" if created else "You are already a valued member of our VIP Club!"

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': msg})

        messages.success(request, msg)
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    return redirect('home')
