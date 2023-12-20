from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.utils.translation import gettext as _  

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a custom user using the UserCreationForm.
    """
    
    # Override the password field
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Your password can't be too similar to your other personal information, must contain at least 8 characters, and can't be a commonly used password.",
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'telephone_number']
