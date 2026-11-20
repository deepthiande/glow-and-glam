from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'address', 'apartment',
            'city', 'state', 'postal_code', 'country',
            'shipping_method', 'payment_method', 'order_notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Jane Doe', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'jane.doe@example.com', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123 Beauty Lane', 'required': True}),
            'apartment': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Apt, Suite, Unit (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'New York', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'NY', 'required': True}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10001', 'required': True}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'United States', 'required': True}),
            'shipping_method': forms.RadioSelect(choices=[
                ('Standard Delivery', 'Standard Delivery (3-5 business days)'),
                ('Express Glam Delivery', 'Express Glam Delivery (1-2 business days) - $15.00')
            ]),
            'payment_method': forms.RadioSelect(choices=[
                ('card', 'Credit / Debit Card (Instant Demo Payment)'),
                ('upi', 'UPI / Online Transfer (Instant Demo Payment)'),
                ('cod', 'Cash on Delivery (Pay at Doorstep)')
            ]),
            'order_notes': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Special delivery notes or gift message...', 'rows': 2}),
        }
