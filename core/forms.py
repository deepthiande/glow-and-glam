from django import forms
from .models import ContactMessage, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email Address', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Phone Number (Optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Subject / Inquiry Type', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-input form-textarea', 'placeholder': 'How can our beauty consultants assist you today?', 'rows': 5, 'required': True}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'newsletter-input', 'placeholder': 'Enter your email for 20% off...', 'required': True}),
        }
