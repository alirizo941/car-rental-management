from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
import random
import string
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=[('', 'Rolni tanlang')] + list(CustomUser.Roles.choices),
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md',
            'placeholder': 'Rolni tanlang'
        }),
        required=True,
        initial=''
    )
    phone = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md',
            'placeholder': '+998 90 123 45 67'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'role', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # CSS klasslari va placeholderlar
        css_class = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md'
        
        self.fields['email'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'email@example.com'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Ismni kiriting'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Familiyani kiriting'
        })

    def generate_username(self, first_name, last_name):
        """Username generatsiya qilish"""
        base_username = f"{first_name.lower()}_{last_name.lower()}"
        username = base_username
        
        # Agar bunday username mavjud bo'lsa, raqam qo'shamiz
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
            
        return username

    def generate_password(self):
        """Xavfsiz parol generatsiya qilish"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for i in range(12))
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Username va parol generatsiya qilish
        username = self.generate_username(user.first_name, user.last_name)
        password = self.generate_password()
        
        user.username = username
        user.password = make_password(password)
        user.is_verified = True  # Avtomatik tasdiqlash
        
        if commit:
            user.save()
            
        return user, password

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_class = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md'
        
        self.fields['first_name'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Ismni kiriting'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Familiyani kiriting'
        })
        self.fields['phone'].widget.attrs.update({
            'class': css_class,
            'placeholder': '+998 90 123 45 67'
        })
