from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Create secure password', 'required': True}),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm your password', 'required': True}),
        min_length=6
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name', 'required': True}),
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your.email@example.com', 'required': True}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username or Email', 'required': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your password', 'required': True})
    )


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'readonly': 'readonly'}))

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'state', 'postal_code', 'country', 'skin_type', 'favorite_category']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State / Province'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Country'}),
            'skin_type': forms.Select(choices=[
                ('Normal', 'Normal'),
                ('Dry', 'Dry'),
                ('Oily', 'Oily'),
                ('Combination', 'Combination'),
                ('Sensitive', 'Sensitive')
            ], attrs={'class': 'form-input'}),
            'favorite_category': forms.Select(choices=[
                ('Lipsticks', 'Lipsticks'),
                ('Foundations', 'Foundations'),
                ('Concealers', 'Concealers'),
                ('Blush', 'Blush'),
                ('Highlighters', 'Highlighters'),
                ('Eyeshadows', 'Eyeshadows'),
                ('Eyeliners', 'Eyeliners'),
                ('Mascaras', 'Mascaras'),
                ('Makeup Brushes', 'Makeup Brushes'),
                ('Skincare', 'Skincare'),
            ], attrs={'class': 'form-input'}),
        }
