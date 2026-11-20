from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm


def register_view(request):
    """User Registration with instant profile creation & login"""
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Log the user in directly
            login(request, user)
            messages.success(request, f"✨ Welcome to the GLOW & GLAM family, {user.first_name or user.username}! Your luxury beauty journey begins now.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User Login supporting username or email"""
    if request.user.is_authenticated:
        return redirect('profile')

    next_url = request.GET.get('next', 'profile')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            # Check if input is email
            user_obj = User.objects.filter(email__iexact=username_or_email).first()
            username = user_obj.username if user_obj else username_or_email

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}! ✨")
                return redirect(next_url if next_url and next_url.startswith('/') else 'profile')
            else:
                messages.error(request, "Invalid username/email or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, "You have been logged out safely. See you soon at GLOW & GLAM!")
    return redirect('home')


@login_required
def profile_view(request):
    """User Profile and Order History"""
    profile = request.user.profile
    orders = Order.objects.filter(user=request.user).prefetch_related('items')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Update user model first and last name
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()

            form.save()
            messages.success(request, "✨ Your beauty profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please check the profile fields.")
    else:
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    active_tab = request.GET.get('tab', 'profile')

    context = {
        'form': form,
        'orders': orders,
        'active_tab': active_tab,
        'user': request.user,
    }
    return render(request, 'accounts/profile.html', context)


def forgot_password_view(request):
    """Demo password reset assistance"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            messages.success(request, f"✨ If an account exists for {email}, a password reset link has been sent. (Demo Mode: You can sign in using sophia / glam123 or admin / admin123).")
            return redirect('login')
        else:
            messages.error(request, "Please provide your registered email address.")
    return render(request, 'accounts/forgot_password.html')
